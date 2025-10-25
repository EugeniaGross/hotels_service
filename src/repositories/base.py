from typing import Any

from pydantic import BaseModel
from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository:
    model = None
    scheme = None
    
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def get_filtered(self, *filter, **filter_by) -> list[BaseModel | Any]:
        query = (
            select(self.model)
            .filter(*filter)
            .filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        return [self.scheme.model_validate(model) for model in result.scalars().all()]
        
    async def get_all(self, *args, **kwargs) -> list[BaseModel | Any]:
        return await self.get_filtered()
    
    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.scheme.model_validate(model)
    
    async def add(self, data: BaseModel):
        stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(stmt)
        return self.scheme.model_validate(result.scalar_one())
    
    async def edit(self, data: BaseModel, exclude_unset, **filter_by):
        stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unset))
            .returning(self.model)
        )
        result = await self.session.execute(stmt)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.scheme.model_validate(model)
    
    async def delete(self, **filter_by):
        stmt = delete(self.model).filter_by(**filter_by).returning(self.model)
        result = await self.session.execute(stmt)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.scheme.model_validate(model)
            