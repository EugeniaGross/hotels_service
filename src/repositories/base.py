from sqlalchemy import insert, select


class BaseRepository:
    model = None
    
    def __init__(self, session):
        self.session = session
        
    async def get_all(self):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def get_one_or_none(self, **filters):
        query = select(self.model).filter_by(**filters)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()
    
    async def add_one(self, data):
        stmt = insert(self.model).values(**data).returning(self.model)
        result = await self.session.execute(stmt)
        return result
            