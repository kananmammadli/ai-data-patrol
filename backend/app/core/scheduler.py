from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import AsyncSessionLocal
from app.models.data_quality import DataQualityCheck
from sqlalchemy.future import select
import asyncio

scheduler = AsyncIOScheduler()

async def run_check(check_id: int):
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(DataQualityCheck).where(DataQualityCheck.id == check_id))
        check = result.scalar_one_or_none()
        if check:
            # Placeholder: actual check execution logic goes here
            print(f"Running check {check.id}: {check.name}")

async def schedule_all_checks():
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(DataQualityCheck))
        checks = result.scalars().all()
        for check in checks:
            if check.schedule:
                scheduler.add_job(
                    run_check,
                    CronTrigger.from_crontab(check.schedule),
                    args=[check.id],
                    id=f"check_{check.id}",
                    replace_existing=True
                )

def start_scheduler():
    scheduler.start()
    asyncio.create_task(schedule_all_checks())
