from typing import Annotated

from fastapi import APIRouter, Query, Body, Depends

from src.api.dependencies import PaginationDep
from src.schemas.hotels import Hotel, HotelPATCH

router = APIRouter(prefix="/hotels", tags=["Отели"])


hotels = [
    {"id": 1, "title": "Dubai", "name": "dubai"},
    {"id": 2, "title": "Sochi", "name": "sochi"},
    {"id": 3, "title": "Mocsow", "name": "mocsow"},
    {"id": 4, "title": "Paris", "name": "paris"},
    {"id": 5, "title": "Berlin", "name": "berlin"},
    {"id": 6, "title": "New York", "name": "new york"},
    {"id": 7, "title": "Kosovo", "name": "kosovo"},
    {"id": 8, "title": "Pekin", "name": "pekin"},
]


@router.get("")
def get_hotels(
    pagination: PaginationDep,
    id: int | None = Query(default=None, description="ID отеля"),
    title: str | None = Query(default=None, description="Название отеля"),
) -> list[Hotel]:
    global hotels
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    return hotels_[(pagination.page - 1) * pagination.per_page: pagination.page * pagination.per_page]


@router.delete("/{hotel_id}")
def delete_hotel(hotel_id: int) -> None:
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "Ok"}   


@router.post("")
def create_hotel(
    hotel: Hotel = Body(openapi_examples={"1": {"summary": "Валидный запрос", "value": {"title": "Moscow", "name": "Mocsow Plaza"}}})
) -> Hotel:
    global hotels
    new_hotel = {"id": hotels[-1]["id"] + 1, "title": hotel.title, "name": hotel.name}
    hotels.append(new_hotel)
    return new_hotel


@router.put("/{hotel_id}")
def update_hotel(
    hotel_id: int,
    hotel: Hotel
) -> Hotel | dict:
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = hotel.title
            hotel["name"] = hotel.name
            return hotel
    return {"error": f"Отеля с id={hotel_id} не существует"}


@router.patch("/{hotel_id}")
def partial_update_hotel(
    hotel_id: int,
    hotel: HotelPATCH
) -> Hotel | dict:
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = hotel.title if hotel.title is not None else hotel["title"]
            hotel["name"] = hotel.name if hotel.name is not None else hotel["name"]
            return hotel
    return {"error": f"Отеля с id={hotel_id} не существует"}
