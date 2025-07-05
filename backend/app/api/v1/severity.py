from fastapi import APIRouter, HTTPException, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.schemas.data_quality import SeverityConfig, SeverityConfigCreate
from app.models.data_quality import SeverityConfig as SeverityConfigModel
from app.core.database import get_db

router = APIRouter(prefix="/severity-configs", tags=["severity-configs"])

@router.post("/", response_model=SeverityConfig)
async def create_severity_config(config: SeverityConfigCreate, db: AsyncSession = Depends(get_db)):
    db_config = SeverityConfigModel(**config.dict())
    db.add(db_config)
    await db.commit()
    await db.refresh(db_config)
    return db_config

@router.get("/{config_id}", response_model=SeverityConfig)
async def get_severity_config(config_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(SeverityConfigModel).where(SeverityConfigModel.id == config_id))
    db_config = result.scalar_one_or_none()
    if not db_config:
        raise HTTPException(status_code=404, detail="Severity config not found")
    return db_config

@router.get("/", response_model=list[SeverityConfig])
async def list_severity_configs(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(SeverityConfigModel))
    return result.scalars().all()

@router.post("/{config_id}/recipients", response_model=SeverityConfig)
async def add_recipient(config_id: int, recipient: str = Body(...), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(SeverityConfigModel).where(SeverityConfigModel.id == config_id))
    db_config = result.scalar_one_or_none()
    if not db_config:
        raise HTTPException(status_code=404, detail="Severity config not found")
    if recipient not in db_config.recipients:
        db_config.recipients.append(recipient)
        await db.commit()
        await db.refresh(db_config)
    return db_config

@router.delete("/{config_id}/recipients", response_model=SeverityConfig)
async def remove_recipient(config_id: int, recipient: str = Body(...), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(SeverityConfigModel).where(SeverityConfigModel.id == config_id))
    db_config = result.scalar_one_or_none()
    if not db_config:
        raise HTTPException(status_code=404, detail="Severity config not found")
    if recipient in db_config.recipients:
        db_config.recipients.remove(recipient)
        await db.commit()
        await db.refresh(db_config)
    return db_config
