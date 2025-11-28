from sqlalchemy import select

from src.repositories.base import BaseRepository
from src.models.users import UsersORM
from src.schemas.users import UserWithHashedPassword
from src.repositories.mappers.mappers import (
    UserDataMapper,
    UserWithHashedPasswordDataMapper,
)


class UsersRepository(BaseRepository):
    model = UsersORM
    mapper = UserDataMapper

    async def get_one_with_hashed_pass(
        self, **filter_by
    ) -> UserWithHashedPassword | None:
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return UserWithHashedPasswordDataMapper.map_to_domain_entity(model)
