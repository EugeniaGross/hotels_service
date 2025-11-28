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
    schema = Hotel


class RoomDataMapper(DataMapper):
    db_model = RoomsORM
    schema = Room


class RoomDataWithRelsMapper(DataMapper):
    db_model = RoomsORM
    schema = RoomWithRels


class UserDataMapper(DataMapper):
    db_model = UsersORM
    schema = User


class UserWithHashedPasswordDataMapper(DataMapper):
    db_model = UsersORM
    schema = UserWithHashedPassword


class BookingDataMapper(DataMapper):
    db_model = BookingsORM
    schema = Bookings


class FacilityDataMapper(DataMapper):
    db_model = FacilitiesORM
    schema = Facility


class RoomFacilityDataMapper(DataMapper):
    db_model = RoomsFacilitiesORM
    schema = RoomFacility
