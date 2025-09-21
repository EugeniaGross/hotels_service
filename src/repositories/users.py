from sqlalchemy import select

from src.repositories.base import BaseRepository
from src.models.users import UsersORM
from src.schemas.users import User, UserWithHashedPassword


class UsersRepository(BaseRepository):
    model = UsersORM
    scheme = User
    
    async def get_one_or_none(self, **filter_by) -> UserWithHashedPassword | None:
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return UserWithHashedPassword.model_validate(model)
    