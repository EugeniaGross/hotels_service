from fastapi import APIRouter, status
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.schemas.facilities import Facility, FacilityAdd
from src.services.facilities import FacilityService

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("")
@cache(expire=60)
async def get_facilities(
    db: DBDep,
) -> list[Facility]:
    return await FacilityService(db).get_facilities()


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_facility(db: DBDep, data: FacilityAdd):
    facility = await FacilityService(db).create_facility(data)
    return {"status": "ok", "data": facility}
