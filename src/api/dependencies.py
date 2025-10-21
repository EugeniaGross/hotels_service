from datetime import date
from typing import Annotated, Optional

from fastapi import Query, Depends, Request, HTTPException, status
from pydantic import BaseModel

from src.database import async_session_maker
from src.services.auth import AuthService
from src.utils.db_manager import DBManager


class PaginationParams(BaseModel):
    page: Annotated[int, Query(default=1, description="Номер страницы", gt=0)]
    per_page: Annotated[int, Query(default=3, description="Количество записей", gt=0, lt=100)]
    
    
class BookingFilters(BaseModel):
    room_id: Optional[Annotated[int, Query(default=None, description="ID комнаты")]] = None
    date_from: Optional[Annotated[int, Query(default=None, description="Дата заселения")]] = None
    date_to: Optional[Annotated[int, Query(default=None, description="Дата выезда")]] = None
    
    
def get_token(request: Request) -> str:
    token = request.cookies.get("access_token")
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail={"error": "токен доступа не обнаружен"}
        )
    return token
    
    
def get_current_user_id(token: str | None = Depends(get_token)):
    data = AuthService().decode_token(token)
    return data.get("id")


def get_db_manager():
    return DBManager(session_factory=async_session_maker)


async def get_db():
    async with get_db_manager() as db:
        yield db
        

DBDep = Annotated[DBManager, Depends(get_db)]    
PaginationDep = Annotated[PaginationParams, Depends()]
BookingFiltersDep = Annotated[BookingFilters, Depends()]
UserIDDep = Annotated[int, Depends(get_current_user_id)]