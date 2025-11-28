from fastapi import APIRouter, Body, status, HTTPException, Response

from src.exceptions import ObjectAlreadyexistsException
from src.schemas.users import UserRequestAdd, UserAdd, User
from src.services.auth import AuthService
from src.api.dependencies import UserIDDep, DBDep


router = APIRouter(prefix="/auth", tags=["Регистрация и аутентификация"])


@router.post("/register")
async def register_user(
    db: DBDep,
    data: UserRequestAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Валидный запрос",
                "value": {"email": "test@example.com", "password": "12345678"},
            }
        }
    ),
) -> dict:
    hashed_password = AuthService().get_hash_password(data.password)
    data = UserAdd(email=data.email, hashed_password=hashed_password)
    try:
        await db.users.add(data)
        await db.commit()
    except ObjectAlreadyexistsException:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "Пользователь уже существует"},
        )
    return {"status": "ok"}


@router.post("/login")
async def login_user(
    db: DBDep,
    response: Response,
    data: UserRequestAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Валидный запрос",
                "value": {"email": "test@example.com", "password": "12345678"},
            }
        }
    ),
) -> dict:
    user = await db.users.get_one_with_hashed_pass(email=data.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Пользователь с таким email не зарегестрирован"},
        )
    if not AuthService().verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Не верный пароль"},
        )
    access_token = AuthService().create_access_token({"id": user.id})
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.get("/me")
async def get_me(db: DBDep, user_id: UserIDDep) -> User | None:
    user = await db.users.get_one_or_none(id=user_id)
    return user


@router.post("/logout")
async def logout(user_id: UserIDDep, response: Response) -> dict:
    response.delete_cookie("access_token")
    return {"status": "ok"}
