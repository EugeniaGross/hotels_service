from fastapi import APIRouter, status, HTTPException

from src.api.dependencies import DBDep, UserIDDep, PaginationDep, BookingFiltersDep
from src.schemas.bookings import BookingsAddRequest, BookingsAdd, Bookings


router = APIRouter(
    prefix="/bookings", 
    tags=["Бронирования"]
)

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_booking(
    db: DBDep,
    user_id: UserIDDep,
    data: BookingsAddRequest
):
    room = await db.rooms.get_one_or_none(
        id=data.room_id
    )
    data = BookingsAdd(**data.model_dump(), user_id=user_id, price=room.price)
    try:
        booking = await db.bookings.add_booking(data, hotel_id=room.hotel_id)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    await db.commit()
    return {"status": "ok", "data": booking}


@router.get("")
async def get_bookings(
    pagination: PaginationDep,
    db: DBDep,
    filters: BookingFiltersDep
) -> list[Bookings]:
    
    bookings = await db.bookings.get_all(
        limit=pagination.per_page, 
        offset=(pagination.page - 1) * pagination.per_page,
        **filters.model_dump(exclude_none=True)
    )
    return bookings


@router.get("/me")
async def get_bookings_me(
    pagination: PaginationDep,
    db: DBDep,
    user_id: UserIDDep,
) -> list[Bookings]:
    
    bookings = await db.bookings.get_all(
        limit=pagination.per_page, 
        offset=(pagination.page - 1) * pagination.per_page,
        user_id=user_id
    )
    return bookings
