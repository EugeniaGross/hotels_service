from fastapi import APIRouter, Query, Body, Depends, status, HTTPException

from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import Room, RoomAdd, RoomPATCH


router = APIRouter(
    prefix="/hotels/{hotel_id}/rooms", 
    tags=["Комнаты"]
)

@router.get("")
async def get_rooms(
    pagination: PaginationDep,
    hotel_id: int
) -> list[Room]:
    async with async_session_maker() as session:
        rooms = await RoomsRepository(session).get_all(
            limit=pagination.per_page, 
            offset=(pagination.page - 1) * pagination.per_page,
            hotel_id=hotel_id
        )
    return rooms


@router.get("/{room_id}")
async def get_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        rooms = await RoomsRepository(session).get_one_or_none(
            id=room_id,
            hotel_id=hotel_id
        )
    if rooms is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return {"status": "ok", "data": rooms} 


@router.delete("/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_room(hotel_id: int, room_id: int) -> None:
    async with async_session_maker() as session:
        hotel = await RoomsRepository(session).delete(
            id=room_id,
            hotel_id=hotel_id
        )
        await session.commit()
    if hotel is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return 


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_room(
    hotel_id: int,
    data: RoomAdd
):
    async with async_session_maker() as session:
        hotel = await RoomsRepository(session).add(
            data,
            hotel_id=hotel_id
        )
        await session.commit()
    return {"status": "ok", "data": hotel}


@router.put("/{room_id}")
async def update_room(
    hotel_id: int,
    room_id: int,
    hotel: Room
):
    async with async_session_maker() as session:
        hotel = await RoomsRepository(session).edit(
            hotel,
            exclude_unset=False,
            id=room_id,
            hotel_id=hotel_id
        )
        await session.commit()
    if hotel is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return {"status": "ok", "data": hotel}


@router.patch("/{room_id}")
async def partial_update_room(
    hotel_id: int,
    room_id: int,
    hotel: RoomPATCH
):
    async with async_session_maker() as session:
        hotel = await RoomsRepository(session).edit(
            hotel,
            exclude_unset=True,
            id=room_id,
            hotel_id=hotel_id
        )
        await session.commit()
    if hotel is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return {"status": "ok", "data": hotel}
