from sqlalchemy import insert, select

from src.repositories.base import BaseRepository
from src.models.hotels import HotelsORM
from src.schemas.hotels import Hotel


class HotelRepository(BaseRepository):
    model = HotelsORM
    scheme = Hotel
    
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
        return [self.scheme.model_validate(model) for model in result.scalars().all()]
    