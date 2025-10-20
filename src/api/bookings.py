from fastapi import APIRouter, status, HTTPException

from src.api.dependencies import DBDep, UserIDDep
from src.schemas.bookings import BookingsCreateRequest, BookingsCreate


router = APIRouter(
    prefix="/bookigs", 
    tags=["Бронирования"]
)

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_booking(
    db: DBDep,
    user_id: UserIDDep,
    data: BookingsCreateRequest
):
    room = await db.rooms.get_one_or_none(
        id=data.room_id
    )
    data = BookingsCreate(**data.model_dump(), user_id=user_id, price=room.price)
    booking = await db.bookings.add(data)
    await db.commit()
    return {"status": "ok", "data": booking}
