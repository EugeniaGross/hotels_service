from fastapi import APIRouter, status
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.schemas.facilities import Facility, FacilityAdd

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("")
@cache(expire=60)
async def get_facilities(
    db: DBDep,
) -> list[Facility]:
    facilities = await db.facilities.get_all()
    return facilities


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_facility(
    db: DBDep,
    data: FacilityAdd
):
    facility = await db.facilities.add(data)
    await db.commit()
    return {"status": "ok", "data": facility}
