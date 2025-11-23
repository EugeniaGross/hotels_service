from datetime import date

from pydantic import BaseModel
from sqlalchemy import select

from src.repositories.base import BaseRepository
from src.models.bookings import BookingsORM
from src.schemas.bookings import Bookings
from src.repositories.mappers.mappers import BookingDataMapper
from src.repositories.utils import rooms_ids_for_booking


class BookingsRepository(BaseRepository):
    model = BookingsORM
    mapper = BookingDataMapper
    
    async def get_all(self, limit, offset, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        query = (
            query
            .offset(offset)
            .limit(limit)
        )
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(model) for model in result.scalars().all()]
    
    async def get_bookings_with_today_checkin(self):
        query = (
            select(BookingsORM)
            .filter(BookingsORM.date_from == date.today())
        )
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(model) for model in result.scalars().all()]
    
    async def add_booking(self, data: BaseModel, hotel_id: int):
        rooms_ids_for_booking_ = rooms_ids_for_booking(
            data.date_from,
            data.date_to,
            hotel_id=hotel_id
        )
        rooms_ids_to_book_res = await self.session.execute(rooms_ids_for_booking_)
        rooms_ids_to_book: list[int] = rooms_ids_to_book_res.scalars().all()
        if data.room_id not in rooms_ids_to_book:
            raise Exception("Этот номер не доступен для бронирования")
        return await super().add(data)
