from src.repositories.base import BaseRepository

from src.models.bookings import BookingsORM
from src.schemas.bookings import Bookings



class BookingsRepository(BaseRepository):
    model = BookingsORM
    scheme = Bookings
    