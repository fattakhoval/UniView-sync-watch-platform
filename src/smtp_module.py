from uuid import UUID, uuid4

from aiosmtplib import send
from sqlalchemy import select
from email.message import EmailMessage
from sqlalchemy.ext.asyncio import AsyncSession

from config import config
from src.manager import room_registry
from src.models import User, Invite, Event, Room, RoomType


class EmailSender:
    def __init__(
            self,
            smtp_host: str,
            smtp_port: int,
            username: str,
            password: str,
            sender_email: str,
            use_tls: bool = True
    ):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.sender_email = sender_email
        self.use_tls = use_tls

    async def send_html_email(
            self,
            to_email: str,
            subject: str,
            html_content: str,
            plain_text: str = "Ваш почтовый клиент не поддерживает HTML."
    ):
        msg = EmailMessage()
        msg["From"] = self.sender_email
        msg["To"] = to_email
        msg["Subject"] = subject

        msg.set_content(plain_text)
        msg.add_alternative(html_content, subtype='html')

        await send(
            msg,
            hostname=self.smtp_host,
            port=self.smtp_port,
            start_tls=self.use_tls,
            username=self.username,
            password=self.password
        )


async def send_recover_password(user_data: User, token: str):

    with open('src/template_emails/reset_password_email.html', 'r', encoding="utf-8") as file:
        html_content = file.read()

    html_content = html_content.format(
        reset_link=f'https://uniview.space/api/user/reset_password?email={user_data.email}&token={token}'
    )

    await mailer.send_html_email(
        to_email=user_data.email,
        subject='Восстановление пароля',
        html_content=html_content,
    )

async def send_first_email(username, event_title, event_datetime, email):

    with open('src/template_emails/invite_email.html', 'r', encoding="utf-8") as file:
        html_content = file.read()

    html_content = html_content.format(
        username=username,
        event_title=event_title,
        event_datetime=event_datetime
    )

    await mailer.send_html_email(to_email=email, subject='Приглашение', html_content=html_content)


async def send_announce(invite_id: UUID, invite_id_event: UUID, session: AsyncSession):

    invite_stmt = select(Invite).where(Invite.id == invite_id)
    invite_result = await session.execute(invite_stmt)
    invite = invite_result.scalar_one_or_none()
    if not invite:
        print(f"[send_announce] Invite {invite_id} not found.")
        return

    event_stmt = select(Event).where(Event.id == invite_id_event)
    event_result = await session.execute(event_stmt)
    event = event_result.scalar_one_or_none()
    if not event:
        print(f"[send_announce] Event {invite_id_event} not found.")
        return

    user_stmt = select(User).where(User.id == invite.id_invited)
    user_result = await session.execute(user_stmt)
    user = user_result.scalar_one_or_none()
    if not user or not user.email:
        print(f"[send_announce] User {invite.id_invited} not found or has no email.")
        return

    room_for_event = Room(
        id_host=user.id,
        name=event.title,
        room_type=RoomType.Public,
    )

    session.add(room_for_event)
    await session.flush()

    with open('src/template_emails/invite_email_repiat.html', 'r', encoding="utf-8") as file:

        html_content = file.read()

    html_content = html_content.format(
        username=user.username,
        event_title=event.title,
        event_datetime=event.datetime_start,
        room_name=event.title,
        invite_link=f'https://uniview.space/room/{room_for_event.id}',
    )

    await mailer.send_html_email(
        to_email=str(user.email),
        subject="Приглашение",
        html_content=html_content
    )

    event.is_second_msg_send = True
    event.id_room = room_for_event.id

    room_registry.add_room(room_id=room_for_event.id)
    await session.commit()
    print(f"[send_announce] Email sent to {user.email} for event {event.id}")


async def send_emails(users_id: list[UUID], event: Event, session: AsyncSession, sender_name: str):

    stmt = select(User).where(User.id.in_(users_id))

    result = await session.execute(stmt)
    users = result.scalars().all()

    for user in users:
        await send_first_email(
            username=sender_name,
            event_title=event.title,
            event_datetime=event.datetime_start.strftime('%d.%m.%Y %H:%M'),
            email=user.email
        )

mailer = EmailSender(
        smtp_host="smtp.yandex.ru",
        smtp_port=587,
        username=config.SMTP_LOGIN,
        password=config.SMTP_PASSWORD,
        sender_email=config.SMTP_LOGIN
    )
