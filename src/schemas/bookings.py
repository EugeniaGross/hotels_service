from datetime import date

from pydantic import BaseModel, ConfigDict


class BookingsCreateRequest(BaseModel):
    date_from: date
    date_to: date
    room_id: int


class BookingsCreate(BookingsCreateRequest):
    user_id: int
    price: int
    
    
class Bookings(BookingsCreateRequest):
    total_cost: int
    user_id: int
    
    model_config = ConfigDict(from_attributes=True)
    