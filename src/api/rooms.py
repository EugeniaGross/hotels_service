from datetime import date

from fastapi import APIRouter, Body, status

from src.api.dependencies import DBDep
from src.exceptions import ObjectNotFoundException, RoomNotFoundHTTPException
from src.schemas.rooms import (
    RoomPatchRequest,
    RoomAddRequest,
    RoomWithRels,
)
from src.services.rooms import RoomService


router = APIRouter(prefix="/hotels/{hotel_id}/rooms", tags=["Комнаты"])


@router.get("")
async def get_rooms(
    db: DBDep, hotel_id: int, date_from: date, date_to: date
) -> list[RoomWithRels]:
    """Получение комнат с фильтрами"""
    return await RoomService(db).get_rooms(hotel_id, date_from, date_to)


@router.get("/{room_id}")
async def get_room(db: DBDep, hotel_id: int, room_id: int) -> dict:
    """Получение одной комнаты по id"""
    try:
        rooms = await RoomService(db).get_room(hotel_id, room_id)
        return {"status": "ok", "data": rooms}
    except ObjectNotFoundException:
        raise RoomNotFoundHTTPException
    


@router.delete("/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_room(db: DBDep, hotel_id: int, room_id: int) -> None:
    """Удаление комнаты"""
    try:
        await RoomService(db).delete_room(hotel_id, room_id)
    except ObjectNotFoundException:
        raise RoomNotFoundHTTPException


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_room(
    db: DBDep, 
    hotel_id: int,
    data: RoomAddRequest = Body(
        openapi_examples={
            "1": {
                "summary": "Валидный запрос",
                "value": {
                    "title": "Все включено", 
                    "description": "Есть все необходимое",
                    "price": 10000,
                    "quantity": 10,
                    "facilities": [1, 2]
                },
            }
        }
    ),
) -> dict:
    """Создание комнаты"""
    room = await RoomService(db).create_room(hotel_id, data)
    return {"status": "ok", "data": room}


@router.put("/{room_id}")
async def update_room(
    db: DBDep, 
    hotel_id: int, 
    room_id: int, 
    data: RoomAddRequest  = Body(
        openapi_examples={
            "1": {
                "summary": "Валидный запрос",
                "value": {
                    "title": "Эконом", 
                    "description": "Бюджетный номер",
                    "price": 2000,
                    "quantity": 11,
                    "facilities": [1]
                },
            }
        }
    ),
):
    """Обновление комнаты"""
    try:
        rooms = await RoomService(db).update_room(hotel_id, room_id, data)
        return {"status": "ok", "data": rooms}
    except ObjectNotFoundException:
        raise RoomNotFoundHTTPException


@router.patch("/{room_id}")
async def partial_update_room(
    db: DBDep, 
    hotel_id: int, 
    room_id: int, 
    data: RoomPatchRequest = Body(
        openapi_examples={
            "1": {
                "summary": "Валидный запрос",
                "value": {
                    "price": 12000,
                    "quantity": 8,
                    "facilities": [3]
                },
            }
        }
    ),
):
    """Частичное обновление комнаты"""
    try:
        rooms = await RoomService(db).partial_update_room(hotel_id, room_id, data)
        return {"status": "ok", "data": rooms}
    except ObjectNotFoundException:
        raise RoomNotFoundHTTPException
