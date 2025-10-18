from sqlalchemy import insert, select
from pydantic import BaseModel

from src.repositories.base import BaseRepository
from src.models.rooms import RoomsORM
from src.schemas.rooms import Room


class RoomsRepository(BaseRepository):
    model = RoomsORM
    scheme = Room
    
    async def get_all(self, limit, offset, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        query = (
            query
            .offset(offset)
            .limit(limit)
        )
        result = await self.session.execute(query)
        return [self.scheme.model_validate(model) for model in result.scalars().all()]
    
    async def add(self, data: BaseModel, hotel_id: int):
        data = data.model_dump()
        data["hotel_id"] = hotel_id
        stmt = insert(self.model).values(**data).returning(self.model)
        result = await self.session.execute(stmt)
        return self.scheme.model_validate(result.scalar_one())