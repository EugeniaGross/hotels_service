from typing import Annotated

from fastapi import Query, Depends, Request, HTTPException, status
from pydantic import BaseModel

from src.services.auth import AuthService


class PaginationParams(BaseModel):
    page: Annotated[int, Query(default=1, description="Номер страницы", gt=0)]
    per_page: Annotated[int, Query(default=3, description="Количество записей", gt=0, lt=100)]
    
    
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
    
    
PaginationDep = Annotated[PaginationParams, Depends()]
UserIDDep = Annotated[int, Depends(get_current_user_id)]