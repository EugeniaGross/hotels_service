from fastapi import APIRouter, status, HTTPException

from src.api.dependencies import DBDep, UserIDDep, PaginationDep, BookingFiltersDep
from src.exceptions import AllRoomsAreBookedException, ObjectNotFoundException, RoomNotFoundHTTPException
from src.schemas.bookings import BookingsAddRequest, Bookings
from src.services.bookings import BookingService


router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_booking(db: DBDep, user_id: UserIDDep, data: BookingsAddRequest):
    try:
        booking = await BookingService(db).create_booking(user_id, data)
        return {"status": "ok", "data": booking}
    except AllRoomsAreBookedException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=exc.detail
        )
    except ObjectNotFoundException:
        raise RoomNotFoundHTTPException


@router.get("")
async def get_bookings(
    pagination: PaginationDep, db: DBDep, filters: BookingFiltersDep
) -> list[Bookings]:
    return await BookingService(db).get_bookings(
        filters,
        limit=pagination.per_page,
        offset=(pagination.page - 1) * pagination.per_page,
    )


@router.get("/me")
async def get_bookings_me(
    pagination: PaginationDep,
    db: DBDep,
    user_id: UserIDDep,
) -> list[Bookings]:
    return await BookingService(db).get_bookings_current_user(
        user_id,
        limit=pagination.per_page,
        offset=(pagination.page - 1) * pagination.per_page,
    )
