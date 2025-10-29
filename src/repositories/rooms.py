from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from src.repositories.base import BaseRepository
from src.repositories.utils import get_rooms_ids_for_booking
from src.models.rooms import RoomsORM
from src.schemas.rooms import Room, RoomWithRels


class RoomsRepository(BaseRepository):
    model = RoomsORM
    scheme = Room
    
    async def get_filterd_by_time(
        self, 
        hotel_id: int, 
        date_from: date, 
        date_to: date, 
    ) -> list[Room]:
        rooms_ids_for_booking = get_rooms_ids_for_booking(
            date_from,
            date_to,
            hotel_id,
        )
        query = (
            select(self.model)
            .options(joinedload(self.model.facilities))
            .filter(RoomsORM.id.in_(rooms_ids_for_booking))
        )
        result = await self.session.execute(query)
        # print(rooms_ids_for_booking.compile(bind=engine, compile_kwargs={"literal_binds": True}))
        return [RoomWithRels.model_validate(model) for model in result.unique().scalars().all()]
    
    async def get_one_or_none(self, **filter_by):
        query = (
            select(self.model)
            .options(joinedload(self.model.facilities))
            .filter_by(**filter_by))
        result = await self.session.execute(query)
        model = result.unique().scalars().one_or_none()
        if model is None:
            return None
        return RoomWithRels.model_validate(model)
    