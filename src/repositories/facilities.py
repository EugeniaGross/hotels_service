from src.repositories.base import BaseRepository
from src.models.facilities import FacilitiesORM, RoomsFacilitiesORM
from src.schemas.facilities import Facility, RoomFacility


class FacilitiesRepository(BaseRepository):
    model = FacilitiesORM
    scheme = Facility


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesORM
    scheme = RoomFacility    