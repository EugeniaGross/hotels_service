from sqlalchemy import insert, select

from src.repositories.base import BaseRepository
from src.models.bookings import BookingsORM
from src.schemas.bookings import Bookings



class BookingsRepository(BaseRepository):
    model = BookingsORM
    scheme = Bookings
    
    async def get_all(self, limit, offset, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        query = (
            query
            .offset(offset)
            .limit(limit)
        )
        result = await self.session.execute(query)
        return [self.scheme.model_validate(model) for model in result.scalars().all()]
    