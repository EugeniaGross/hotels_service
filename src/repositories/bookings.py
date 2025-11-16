from datetime import date

from sqlalchemy import insert, select

from src.repositories.base import BaseRepository
from src.models.bookings import BookingsORM
from src.schemas.bookings import Bookings
from src.repositories.mappers.mappers import BookingDataMapper


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
     