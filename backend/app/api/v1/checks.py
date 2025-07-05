from fastapi import APIRouter, HTTPException, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.schemas.data_quality import DataQualityCheck, DataQualityCheckCreate
from app.models.data_quality import DataQualityCheck as DataQualityCheckModel
from app.core.database import get_db
from app.core.sql_validation import validate_sql_syntax

router = APIRouter(prefix="/checks", tags=["checks"])

@router.post("/", response_model=DataQualityCheck)
async def create_check(check: DataQualityCheckCreate, db: AsyncSession = Depends(get_db)):
    db_check = DataQualityCheckModel(**check.dict())
    db.add(db_check)
    await db.commit()
    await db.refresh(db_check)
    return db_check

@router.put("/{check_id}", response_model=DataQualityCheck)
async def update_check(check_id: int, check: DataQualityCheckCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(DataQualityCheckModel).where(DataQualityCheckModel.id == check_id))
    db_check = result.scalar_one_or_none()
    if not db_check:
        raise HTTPException(status_code=404, detail="Check not found")
    for key, value in check.dict().items():
        setattr(db_check, key, value)
    await db.commit()
    await db.refresh(db_check)
    return db_check

@router.get("/{check_id}", response_model=DataQualityCheck)
async def get_check(check_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(DataQualityCheckModel).where(DataQualityCheckModel.id == check_id))
    db_check = result.scalar_one_or_none()
    if not db_check:
        raise HTTPException(status_code=404, detail="Check not found")
    return db_check

@router.get("/", response_model=list[DataQualityCheck])
async def list_checks(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(DataQualityCheckModel))
    return result.scalars().all()

@router.post("/validate-sql")
async def validate_sql(query: dict):
    sql = query.get("query")
    is_valid, error = validate_sql_syntax(sql)
    if is_valid:
        return {"valid": True}
    return {"valid": False, "error": error}

@router.get("/{check_id}/expiry", response_model=int)
async def get_expiry_period(check_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(DataQualityCheckModel).where(DataQualityCheckModel.id == check_id))
    db_check = result.scalar_one_or_none()
    if not db_check:
        raise HTTPException(status_code=404, detail="Check not found")
    return db_check.expiry_period

@router.put("/{check_id}/expiry", response_model=int)
async def update_expiry_period(check_id: int, expiry_period: int = Body(...), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(DataQualityCheckModel).where(DataQualityCheckModel.id == check_id))
    db_check = result.scalar_one_or_none()
    if not db_check:
        raise HTTPException(status_code=404, detail="Check not found")
    db_check.expiry_period = expiry_period
    await db.commit()
    await db.refresh(db_check)
    return db_check.expiry_period
