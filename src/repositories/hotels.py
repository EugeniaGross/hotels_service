from sqlalchemy import insert, select

from src.repositories.base import BaseRepository
from src.models.hotels import HotelsORM


class HotelRepository(BaseRepository):
    model = HotelsORM
    
    async def get_all(self, location, title, limit, offset):
        query = select(self.model)
        if title:
            query = query.where(self.model.title.icontains(title))
        if location:
            query = query.where(self.model.location.icontains(location))
        query = (
            query
            .offset(offset)
            .limit(limit)
        )
        result = await self.session.execute(query)
        return result.scalars().all()
    