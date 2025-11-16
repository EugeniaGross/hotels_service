from src.models.bookings import BookingsORM
from src.models.facilities import FacilitiesORM, RoomsFacilitiesORM
from src.models.hotels import HotelsORM
from src.models.rooms import RoomsORM
from src.models.users import UsersORM
from src.repositories.mappers.base import DataMapper
from src.schemas.bookings import Bookings
from src.schemas.facilities import Facility, RoomFacility
from src.schemas.hotels import Hotel
from src.schemas.rooms import Room, RoomWithRels
from src.schemas.users import User, UserWithHashedPassword


class HotelDataMapper(DataMapper):
    db_model = HotelsORM
    scheme = Hotel


class RoomDataMapper(DataMapper):
    db_model = RoomsORM
    scheme = Room


class RoomDataWithRelsMapper(DataMapper):
    db_model = RoomsORM
    scheme = RoomWithRels


class UserDataMapper(DataMapper):
    db_model = UsersORM
    scheme = User
    
    
class UserWithHashedPasswordDataMapper(DataMapper):
    db_model = UsersORM
    scheme = UserWithHashedPassword


class BookingDataMapper(DataMapper):
    db_model = BookingsORM
    scheme = Bookings


class FacilityDataMapper(DataMapper):
    db_model = FacilitiesORM
    scheme = Facility


class RoomFacilityDataMapper(DataMapper):
    db_model = RoomsFacilitiesORM
    scheme = RoomFacility
    