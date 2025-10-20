from fastapi import APIRouter, status, HTTPException

from src.api.dependencies import PaginationDep, DBDep
from src.schemas.rooms import Room, RoomAdd, RoomPATCH


router = APIRouter(
    prefix="/hotels/{hotel_id}/rooms", 
    tags=["Комнаты"]
)

@router.get("")
async def get_rooms(
    db: DBDep,
    pagination: PaginationDep,
    hotel_id: int
) -> list[Room]:
    rooms = await db.rooms.get_all(
        limit=pagination.per_page, 
        offset=(pagination.page - 1) * pagination.per_page,
        hotel_id=hotel_id
    )
    return rooms


@router.get("/{room_id}")
async def get_room(db: DBDep, hotel_id: int, room_id: int):
    rooms = await db.rooms.get_one_or_none(
        id=room_id,
        hotel_id=hotel_id
    )
    if rooms is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return {"status": "ok", "data": rooms} 


@router.delete("/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_room(db: DBDep, hotel_id: int, room_id: int) -> None:
    hotel = await db.rooms.delete(
        id=room_id,
        hotel_id=hotel_id
    )
    await db.commit()
    if hotel is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return 


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_room(
    db: DBDep,
    hotel_id: int,
    data: RoomAdd
):
    hotel = await db.rooms.add(
        data,
        hotel_id=hotel_id
    )
    await db.commit()
    return {"status": "ok", "data": hotel}


@router.put("/{room_id}")
async def update_room(
    db: DBDep,
    hotel_id: int,
    room_id: int,
    hotel: Room
):
    hotel = await db.rooms.edit(
        hotel,
        exclude_unset=False,
        id=room_id,
        hotel_id=hotel_id
    )
    await db.commit()
    if hotel is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return {"status": "ok", "data": hotel}


@router.patch("/{room_id}")
async def partial_update_room(
    db: DBDep,
    hotel_id: int,
    room_id: int,
    hotel: RoomPATCH
):
    hotel = await db.rooms.edit(
        hotel,
        exclude_unset=True,
        id=room_id,
        hotel_id=hotel_id
    )
    await db.commit()
    if hotel is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return {"status": "ok", "data": hotel}
