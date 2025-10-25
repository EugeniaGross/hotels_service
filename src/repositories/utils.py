from datetime import date

from sqlalchemy import select, func

from src.models.bookings import BookingsORM
from src.models.rooms import RoomsORM


def get_rooms_ids_for_booking(
    date_from: date, 
    date_to: date, 
    hotel_id: int | None = None, 
    ):
    rooms_count = (
        select(BookingsORM.room_id, func.count("*").label("rooms_booked"))
        .select_from(BookingsORM)
        .filter(
            BookingsORM.date_from <= date_from, 
            BookingsORM.date_to >= date_to
        )
        .group_by(BookingsORM.room_id)
        .cte(name="rooms_count")
    )
    rooms_left_table = (
        select(
            RoomsORM.id.label("room_id"), 
            RoomsORM.quantity - func.coalesce(rooms_count.c.rooms_booked, 0).label("rooms_left")
        )
        .select_from(RoomsORM)
        .outerjoin(rooms_count, RoomsORM.id == rooms_count.c.room_id)
        .cte(name="rooms_left_table")
    )
    rooms_ids_by_hotel = (
        select(RoomsORM.id)
        .select_from(RoomsORM)
    )
    if hotel_id:
        rooms_ids_by_hotel.filter_by(hotel_id=hotel_id)
    rooms_ids_by_hotel.subquery(name="rooms_ids_by_hotel")
    query = (
        select(rooms_left_table.c.room_id)
        .select_from(rooms_left_table)
        .filter(
            rooms_left_table.c.rooms_left > 0,
            rooms_left_table.c.room_id.in_(rooms_ids_by_hotel)
        )
    )
    return query
