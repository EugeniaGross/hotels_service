from src.schemas.facilities import Facility, FacilityAdd
from src.services.base import BaseService


class FacilityService(BaseService):
    async def get_facilities(self) -> list[Facility]:
        facilities = await self.db.facilities.get_all()
        return facilities
    
    async def create_facility(self, data: FacilityAdd):
        facility = await self.db.facilities.add(data)
        await self.db.commit()
        return facility