from datetime import datetime, timedelta
from typing import Callable, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from apscheduler.triggers.date import DateTrigger
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.memory import MemoryJobStore

from src.db import get_db
from src.models import Invite, Event
from src.smtp_module import send_announce


class Tasker:

    def __init__(self):

        self.jobstores ={
            'default': MemoryJobStore()
        }

        self.scheduler = AsyncIOScheduler(
            jobstores=self.jobstores
        )

    def start(self):
        if not self.scheduler.running:
            self.scheduler.start()

        self.scheduler.add_job(
            self.run_watch_invites,
            trigger='interval',
            minutes=1,
            id='periodic_watch_invites',
            replace_existing=True
        )

    def shutdown(self, wait=True):
        self.scheduler.shutdown(wait=wait)

    def add_task(
            self,
            run_date: datetime,
            func: Callable,
            args: Optional[tuple] = None,
            kwargs: Optional[dict] = None,
            job_id: Optional[str] = None
    ):

        trigger = DateTrigger(run_date=run_date)

        return self.scheduler.add_job(
            func=func,
            trigger=trigger,
            args=args or (),
            kwargs=kwargs or {},
            id=job_id
        )

    async def watch_invites(self, session: AsyncSession):
        stmt = (
            select(Invite, Event.datetime_start)
            .join(Event, Invite.id_event == Event.id)
            .where(Event.is_second_msg_send == False)
        )
        result = await session.execute(stmt)
        rows = result.all()

        print(rows)

        for invite, datetime_start in rows:
            job_id = str(invite.id)
            if not self.scheduler.get_job(job_id):
                run_at = datetime_start - timedelta(hours=1)

                if run_at > datetime.now():
                    print(f'Create Task for {job_id} - {run_at}')
                    self.scheduler.add_job(
                        func=self.run_send_announce_task,
                        trigger=DateTrigger(run_date=run_at),
                        args=[str(invite.id), str(invite.id_event)],
                        id=job_id
                    )

    async def run_watch_invites(self):
        print('!!!Run period task!!!')
        async for session in get_db():
            await self.watch_invites(session)

    @staticmethod
    async def run_send_announce_task(invite_id: str, event_id: str):
        async for session in get_db():
            await send_announce(UUID(invite_id), UUID(event_id), session)


tasker = Tasker()
