from datetime import date

from fastapi import APIRouter, Query, Body, status, HTTPException
from fastapi_cache.decorator import cache

from src.api.dependencies import PaginationDep, DBDep
from src.exceptions import ObjectNotFoundException, HotelNotFoundHTTPException
from src.schemas.hotels import Hotel, HotelPATCH
from src.services.hotels import HotelService

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
@cache(expire=60)
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    date_from: date,
    date_to: date,
    location: str | None = Query(default=None, description="Адрес отеля"),
    title: str | None = Query(default=None, description="Название отеля"),
) -> list[Hotel]:
    """Получение отелей по фильтру"""
    return await HotelService(db).get_hotels(
        date_from=date_from,
        date_to=date_to,
        location=location,
        title=title,
        limit=pagination.per_page,
        offset=(pagination.page - 1) * pagination.per_page,
    )


@router.get("/{hotel_id}")
async def get_hotel(
    hotel_id: int,
    db: DBDep,
) -> dict:
    """Получение отеля по id"""
    try:
        hotel = await HotelService(db).get_hotel(hotel_id)
        return {"status": "ok", "data": hotel}
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException
    


@router.delete("/{hotel_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_hotel(
    hotel_id: int,
    db: DBDep,
) -> None:
    """Удаление отеля"""
    try:
        await HotelService(db).delete_hotel(hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_hotel(
    db: DBDep,
    data: Hotel = Body(
        openapi_examples={
            "1": {
                "summary": "Валидный запрос",
                "value": {"title": "Mocsow Plaza", "location": "Москва"},
            }
        }
    ),
) -> dict:
    """Создание отеля"""
    hotel = await HotelService(db).create_hotel(data)
    return {"status": "ok", "data": hotel}


@router.put("/{hotel_id}")
async def update_hotel(
    db: DBDep, 
    hotel_id: int, 
    hotel: Hotel = Body(
        openapi_examples={
            "1": {
                "summary": "Валидный запрос",
                "value": {"title": "Ligovsiy", "location": "Санкт-Петербург"},
            }
        }
    )
) -> dict:
    """Полное обновление отеля"""
    try:
        hotel = await HotelService(db).update_hotel(hotel_id, hotel)
        return {"status": "ok", "data": hotel}
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException
    


@router.patch("/{hotel_id}")
async def partial_update_hotel(
    db: DBDep, 
    hotel_id: int, 
    hotel: HotelPATCH = Body(
        openapi_examples={
            "1": {
                "summary": "Валидный запрос",
                "value": {"title": "5 star"},
            }
        }
    )
) -> dict:
    """Частичное обновление отеля"""
    try:
        hotel = await HotelService(db).partial_update_hotel(hotel_id, hotel)
        return {"status": "ok", "data": hotel}
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException
