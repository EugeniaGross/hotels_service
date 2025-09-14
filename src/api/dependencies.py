from typing import Annotated

from fastapi import Query, Depends
from pydantic import BaseModel


class PaginationParams(BaseModel):
    page: Annotated[int, Query(default=1, description="Номер страницы", gt=0)]
    per_page: Annotated[int, Query(default=3, description="Количество записей", gt=0, lt=100)]
    
    
PaginationDep = Annotated[PaginationParams, Depends()]