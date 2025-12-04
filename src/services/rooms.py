from datetime import date
from src.exceptions import ObjectNotFoundException, check_date_to_after_date_from
from src.schemas.facilities import RoomFacilityAdd
from src.schemas.rooms import RoomAdd, RoomAddRequest, RoomPatch, RoomPatchRequest, RoomWithRels
from src.services.base import BaseService


class RoomService(BaseService):
    async def get_rooms(
        self, hotel_id: int, date_from: date, date_to: date
    ) -> list[RoomWithRels]:
        check_date_to_after_date_from(date_from, date_to)
        rooms = await self.db.rooms.get_filterd_by_time(
            hotel_id=hotel_id, date_from=date_from, date_to=date_to
        )
        return rooms
    
    async def get_room(self, hotel_id: int, room_id: int):
        rooms = await self.db.rooms.get_one_or_none_with_rel(id=room_id, hotel_id=hotel_id)
        if rooms is None:
            raise ObjectNotFoundException
        return rooms
    
    async def delete_room(self, hotel_id: int, room_id: int) -> None:
        hotel = await self.db.rooms.delete(id=room_id, hotel_id=hotel_id)
        await self.db.commit()
        if hotel is None:
            raise ObjectNotFoundException
        
    async def create_room(self, hotel_id: int, data: RoomAddRequest):
        _data = RoomAdd(hotel_id=hotel_id, **data.model_dump())
        room = await self.db.rooms.add(_data)
        rooms_facilities = [
            RoomFacilityAdd(room_id=room.id, facility_id=facility_id)
            for facility_id in data.facilities_ids
        ]
        if rooms_facilities:
            await self.db.rooms_facilities.add_bulk(rooms_facilities)
        await self.db.commit()
        return room
    
    async def update_room(self, hotel_id: int, room_id: int, data: RoomAddRequest):
        _data = RoomAdd(hotel_id=hotel_id, **data.model_dump())
        room = await self.db.rooms.edit(
            _data,
            exclude_unset=False,
            id=room_id,
        )
        await self.db.rooms_facilities.set_room_fasilities(room_id, data.facilities_ids)
        await self.db.commit()
        if room is None:
            raise ObjectNotFoundException
        return room
    
    async def partial_update_room(
        self, hotel_id: int, room_id: int, data: RoomPatchRequest
    ):
        _data_dict = data.model_dump(exclude_unset=True)
        _data = RoomPatch(hotel_id=hotel_id, **_data_dict)
        room = await self.db.rooms.edit(_data, exclude_unset=True, id=room_id)
        if "facilities_ids" in _data_dict:
            await self.db.rooms_facilities.set_room_fasilities(room_id, data.facilities_ids)
        await self.db.commit()
        if room is None:
            raise ObjectNotFoundException
        return room
