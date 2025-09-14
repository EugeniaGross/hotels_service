from pydantic import BaseModel
from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository:
    model = None
    
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def get_all(self):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()
    
    async def add(self, data: BaseModel):
        stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(stmt)
        return result.scalar_one()
    
    async def edit(self, data: BaseModel, **filter_by):
        stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=True))
            .returning(self.model)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def delete(self, **filter_by):
        stmt = delete(self.model).filter_by(**filter_by).returning(self.model)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
            