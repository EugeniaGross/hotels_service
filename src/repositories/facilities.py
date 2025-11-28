from sqlalchemy import select, delete

from src.repositories.base import BaseRepository
from src.models.facilities import FacilitiesORM, RoomsFacilitiesORM
from src.schemas.facilities import RoomFacilityAdd
from src.repositories.mappers.mappers import FacilityDataMapper, RoomFacilityDataMapper


class FacilitiesRepository(BaseRepository):
    model = FacilitiesORM
    mapper = FacilityDataMapper


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesORM
    mapper = RoomFacilityDataMapper

    async def set_room_fasilities(self, room_id: int, facilities_ids: list[int]):
        query = (
            select(self.model.facility_id)
            .select_from(self.model)
            .filter_by(room_id=room_id)
        )
        result = await self.session.execute(query)
        current_facilities_ids = result.scalars().all()
        facilities_for_del = set(current_facilities_ids) - set(facilities_ids)
        facilities_for_insert = set(facilities_ids) - set(current_facilities_ids)
        if facilities_for_del:
            query = delete(self.model).filter(
                self.model.room_id == room_id,
                self.model.facility_id.in_(facilities_for_del),
            )
            await self.session.execute(query)
        if facilities_for_insert:
            await self.add_bulk(
                [
                    RoomFacilityAdd(room_id=room_id, facility_id=facility_id)
                    for facility_id in facilities_for_insert
                ]
            )
