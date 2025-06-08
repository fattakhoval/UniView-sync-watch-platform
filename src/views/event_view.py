from datetime import datetime
from uuid import UUID

from sqlalchemy import select
from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_db
from src.models import Event, Invite, User
from src.schemas import EventCreate, EventOut
from src.smtp_module import send_emails

event_view = APIRouter(prefix='/event')


@event_view.post('/create')
async def create_event(data: EventCreate, session: AsyncSession = Depends(get_db)):
    data_dict = data.model_dump()
    datetime_str = f"{data_dict.pop('date')}T{data_dict.pop('time')}"
    data_dict['datetime_start'] = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S')
    invited_list = data_dict.pop('invited_list')
    new_event = Event(**data_dict)

    session.add(new_event)
    await session.flush()

    invites = []
    for invited_user in invited_list:
        invites.append(Invite(
            id_event=new_event.id,
            id_inviter=new_event.id_creator,
            id_invited=invited_user
        ))

    session.add_all(invites)

    creator = await session.get(User, data.id_creator)

    await send_emails(invited_list, new_event, session, str(creator.username))

    await session.commit()

    return JSONResponse(status_code=201, content={'Status': True})


@event_view.get('/user_event/{user_id}')
async def get_events_by_user(user_id: str, session: AsyncSession = Depends(get_db)):

    stmt = select(Event).where(Event.id_creator == UUID(user_id))

    result = await session.execute(stmt)

    events = result.scalars().all()

    return JSONResponse(
        status_code=201,
        content=[EventOut(**event.__dict__).model_dump(mode='json') for event in events]
    )
