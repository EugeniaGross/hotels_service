from datetime import date

from pydantic import BaseModel, ConfigDict


class BookingsAddRequest(BaseModel):
    date_from: date
    date_to: date
    room_id: int


class BookingsAdd(BookingsAddRequest):
    user_id: int
    price: int


class Bookings(BookingsAddRequest):
    id: int
    total_cost: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)
