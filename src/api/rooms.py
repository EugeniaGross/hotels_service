from datetime import date

from fastapi import APIRouter, status, HTTPException

from src.api.dependencies import DBDep
from src.schemas.rooms import Room, RoomAdd, RoomPatch, RoomPatchRequest, RoomAddRequest, RoomWithRels
from src.schemas.facilities import RoomFacilityAdd


router = APIRouter(
    prefix="/hotels/{hotel_id}/rooms", 
    tags=["Комнаты"]
)

@router.get("")
async def get_rooms(
    db: DBDep,
    hotel_id: int,
    date_from: date,
    date_to: date
) -> list[RoomWithRels]:
    rooms = await db.rooms.get_filterd_by_time(
        hotel_id=hotel_id,
        date_from=date_from,
        date_to=date_to
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
    data: RoomAddRequest
):
    _data = RoomAdd(hotel_id=hotel_id, **data.model_dump())
    room = await db.rooms.add(
        _data
    )
    rooms_facilities = [
        RoomFacilityAdd(room_id=room.id, facility_id=facility_id)
        for facility_id in data.facilities_ids
    ]
    await db.rooms_facilities.add_bulk(rooms_facilities)
    await db.commit()
    return {"status": "ok", "data": room}


@router.put("/{room_id}")
async def update_room(
    db: DBDep,
    hotel_id: int,
    room_id: int,
    data: RoomAddRequest
):
    _data = RoomAdd(hotel_id=hotel_id, **data.model_dump())
    room = await db.rooms.edit(
        _data,
        exclude_unset=False,
        id=room_id,
    )
    await db.rooms_facilities.set_room_fasilities(room_id, data.facilities_ids)
    await db.commit()
    if room is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return {"status": "ok", "data": room}


@router.patch("/{room_id}")
async def partial_update_room(
    db: DBDep,
    hotel_id: int,
    room_id: int,
    data: RoomPatchRequest
):
    _data_dict = data.model_dump(exclude_unset=True)
    _data = RoomPatch(hotel_id=hotel_id, **_data_dict)
    room = await db.rooms.edit(
        _data,
        exclude_unset=True,
        id=room_id
    )
    if "facilities_ids" in _data_dict:
        await db.rooms_facilities.set_room_fasilities(room_id, data.facilities_ids)
    await db.commit()
    if room is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return {"status": "ok", "data": room}
