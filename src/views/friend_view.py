from uuid import UUID

from sqlalchemy import select, insert, update, or_, and_, delete
from fastapi import APIRouter, Depends, Body
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_db
from src.models import Friendship, FriendshipStatus, User
from src.schemas import FriendPending, Friend

friend_view = APIRouter(prefix='/friend')


@friend_view.post('/request')
async def request_friend(name_or_email: str = Body(...), current_user: UUID = Body(...), session: AsyncSession = Depends(get_db)):
    exists_stmt = select(User).where(or_(User.username == name_or_email, User.email == name_or_email))

    result = await session.execute(exists_stmt)
    target_user = result.scalars().one_or_none()

    if not target_user:
        return JSONResponse(status_code=404, content={'Error': f'User with name or email: {name_or_email} not found'})

    if target_user.id == current_user:
        return JSONResponse(
            status_code=400,
            content={'error': 'Нельзя добавить самого себя в друзья.'}
        )

    check_stmt = select(Friendship).where(
        Friendship.id_requester == current_user,
        Friendship.id_addressee == target_user.id
    )
    result = await session.execute(check_stmt)
    existing = result.scalar_one_or_none()

    if existing:
        return JSONResponse(
            status_code=400,
            content={'error': 'Пользователь уже добавлен или ожидает подтверждения.'}
        )

    reverse_stmt = select(Friendship).where(
        Friendship.id_requester == target_user.id,
        Friendship.id_addressee == current_user
    )
    result = await session.execute(reverse_stmt)
    reverse_request = result.scalar_one_or_none()

    if reverse_request:
        update_stmt = (
            update(Friendship)
            .where(Friendship.id == reverse_request.id)
            .values(status=FriendshipStatus.Accepted)
        )
        await session.execute(update_stmt)
        await session.commit()
        return JSONResponse(
            status_code=200,
            content={'result': 'Заявка автоматически подтверждена.'}
        )

    stmt = insert(Friendship).values(
        id_requester=current_user,
        id_addressee=target_user.id
    )

    await session.execute(stmt)
    await session.commit()

    return JSONResponse(status_code=201, content={'result': True})


@friend_view.post('/accept')
async def accept_friend(id_requester: UUID = Body(...), current_user: UUID = Body(...), session: AsyncSession = Depends(get_db)):
    stmt = (
        update(Friendship)
        .where(Friendship.id_requester == id_requester, Friendship.id_addressee == current_user)
        .values(status=FriendshipStatus.Accepted)
    )

    await session.execute(stmt)
    await session.commit()

    return JSONResponse(status_code=200, content={'result': True})


@friend_view.post('/decline')
async def cancel_friend(id_requester: UUID = Body(...), current_user: UUID = Body(...), session: AsyncSession = Depends(get_db)):
    stmt = (
        update(Friendship)
        .where(Friendship.id_requester == id_requester, Friendship.id_addressee == current_user)
        .values(status=FriendshipStatus.Declined)
    )

    await session.execute(stmt)
    await session.commit()

    return JSONResponse(status_code=200, content={'result': True})


@friend_view.get('/friends/{current_user}', response_model=list[Friend])
async def get_friends(current_user: UUID, session: AsyncSession = Depends(get_db)):
    stms = select(User).join(
        Friendship,
        ((Friendship.id_requester == current_user) & (Friendship.id_addressee == User.id)) |
        ((Friendship.id_addressee == current_user) & (Friendship.id_requester == User.id))
    ).where(Friendship.status == FriendshipStatus.Accepted)

    result = await session.execute(stms)
    friends = result.scalars().all()

    return JSONResponse(status_code=200, content=[Friend.model_validate({**friend.__dict__}).model_dump(mode='json') for friend in friends])


@friend_view.get('/pending/{current_user}', response_model=list[FriendPending])
async def get_pending_friends(current_user: UUID, session: AsyncSession = Depends(get_db)):
    stms = select(User, Friendship.status).join(
        Friendship,
        ((Friendship.id_addressee == current_user) & (Friendship.id_requester == User.id))
    ).where(Friendship.status == FriendshipStatus.Pending)

    result = await session.execute(stms)
    rows = result.all()

    for row, status in rows:
        row.__dict__['status'] = status

    return [row[0].__dict__ for row in rows]


@friend_view.post('/remove')
async def remove_friend(target_user_id: UUID = Body(...), current_user: UUID = Body(...), session: AsyncSession = Depends(get_db)):
    delete_stmt = delete(Friendship).where(
        or_(
            and_(
                Friendship.id_requester == current_user,
                Friendship.id_addressee == target_user_id
            ),
            and_(
                Friendship.id_requester == target_user_id,
                Friendship.id_addressee == current_user
            )
        )
    )

    result = await session.execute(delete_stmt)
    await session.commit()

    if result.rowcount == 0:
        return JSONResponse(
            status_code=404,
            content={'error': 'Дружба не найдена.'}
        )

    return JSONResponse(status_code=200, content={'result': True})


