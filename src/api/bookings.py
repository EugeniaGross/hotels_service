from fastapi import APIRouter, status, HTTPException

from src.api.dependencies import DBDep, UserIDDep, PaginationDep, BookingFiltersDep
from src.exceptions import AllRoomsAreBookedException, ObjectNotFoundException
from src.models import RoomsORM
from src.schemas.bookings import BookingsAddRequest, BookingsAdd, Bookings


router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_booking(db: DBDep, user_id: UserIDDep, data: BookingsAddRequest):
    room: RoomsORM | None = await db.rooms.get_one_or_none(id=data.room_id)
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Номер не найден"
        )
    data = BookingsAdd(**data.model_dump(), user_id=user_id, price=room.price)
    try:
        booking = await db.bookings.add_booking(data, hotel_id=room.hotel_id)
    except AllRoomsAreBookedException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=exc.detail
        )
    await db.commit()
    return {"status": "ok", "data": booking}


@router.get("")
async def get_bookings(
    pagination: PaginationDep, db: DBDep, filters: BookingFiltersDep
) -> list[Bookings]:
    bookings = await db.bookings.get_all(
        limit=pagination.per_page,
        offset=(pagination.page - 1) * pagination.per_page,
        **filters.model_dump(exclude_none=True),
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
        user_id=user_id,
    )
    return bookings
