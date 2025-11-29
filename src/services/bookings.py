from src.api.dependencies import BookingFiltersDep
from src.exceptions import AllRoomsAreBookedException, ObjectNotFoundException
from src.models.rooms import RoomsORM
from src.schemas.bookings import Bookings, BookingsAdd, BookingsAddRequest
from src.services.base import BaseService


class BookingService(BaseService):
    async def create_booking(self, user_id: int, data: BookingsAddRequest):
        room: RoomsORM | None = await self.db.rooms.get_one_or_none(id=data.room_id)
        if not room:
            raise ObjectNotFoundException
        data = BookingsAdd(**data.model_dump(), user_id=user_id, price=room.price)
        booking = await self.db.bookings.add_booking(data, hotel_id=room.hotel_id)
        await self.db.commit()
        return booking
    
    async def get_bookings(self, filters: BookingFiltersDep, limit: int, offset: int) -> list[Bookings]:
        bookings = await self.db.bookings.get_all(
            limit=limit,
            offset=offset,
            **filters.model_dump(exclude_none=True),
        )
        return bookings
    
    async def get_bookings_current_user(
        self,
        user_id: int,
        limit: int,
        offset: int
    ) -> list[Bookings]:
        bookings = await self.db.bookings.get_all(
            limit=limit,
            offset=offset,
            user_id=user_id,
        )
        return bookings