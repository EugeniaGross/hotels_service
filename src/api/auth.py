from fastapi import APIRouter, Query, Body, Depends, status, HTTPException
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError

from src.schemas.users import UserRequestAdd, UserAdd, User
from src.database import async_session_maker
from src.repositories.users import UsersRepository

router = APIRouter(prefix="/auth", tags=["Регистрация и аутентификация"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_hash_password(password: str) -> str:
    return pwd_context.hash(password)


@router.post("/register")
async def register_user(
    data: UserRequestAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Валидный запрос", 
                "value": {"email": "test@example.com", "password": "12345678"}
            }
        }
    )
):
    hashed_password = get_hash_password(data.password)
    data = UserAdd(email=data.email, hashed_password=hashed_password)
    try:
        async with async_session_maker() as session:
            user = await UsersRepository(session).add(
                data
            )
            await session.commit()
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail={"error": "Пользователь уже существует"}
        )
    return {"status": "ok"}
