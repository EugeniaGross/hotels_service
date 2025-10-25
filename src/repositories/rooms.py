from datetime import date

from sqlalchemy import insert
from pydantic import BaseModel

from src.database import engine
from src.repositories.base import BaseRepository
from src.repositories.utils import get_rooms_ids_for_booking
from src.models.rooms import RoomsORM
from src.schemas.rooms import Room


class RoomsRepository(BaseRepository):
    model = RoomsORM
    scheme = Room
    
    async def get_filterd_by_time(
        self, 
        hotel_id: int, 
        date_from: date, 
        date_to: date, 
    ):
        rooms_ids_for_booking = get_rooms_ids_for_booking(
            date_from,
            date_to,
            hotel_id,
        )
        # print(rooms_ids_for_booking.compile(bind=engine, compile_kwargs={"literal_binds": True}))
        return await self.get_filtered(RoomsORM.id.in_(rooms_ids_for_booking))
    
    async def add(self, data: BaseModel, hotel_id: int):
        data = data.model_dump()
        data["hotel_id"] = hotel_id
        stmt = insert(self.model).values(**data).returning(self.model)
        result = await self.session.execute(stmt)
        return self.scheme.model_validate(result.scalar_one())