from typing import Annotated

from fastapi import APIRouter, Query, Body, Depends, status
from sqlalchemy import insert, select

from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.models.hotels import HotelsORM
from src.schemas.hotels import Hotel, HotelPATCH

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
async def get_hotels(
    pagination: PaginationDep,
    location: str | None = Query(default=None, description="Адрес отеля"),
    title: str | None = Query(default=None, description="Название отеля"),
) -> list[Hotel]:
    async with async_session_maker() as session:
        query = select(HotelsORM)
        if title:
            query = query.where(HotelsORM.title.icontains(title))
        if location:
            query = query.where(HotelsORM.location.icontains(location))
        query = (
            query
            .offset((pagination.page - 1) * pagination.per_page)
            .limit(pagination.per_page)
        )
        print(query.compile())
        result = await session.execute(query)
        hotels = result.scalars().all()
    return hotels


@router.delete("/{hotel_id}")
def delete_hotel(hotel_id: int) -> None:
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "ok"}   


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_hotel(
    hotel: Hotel = Body(
        openapi_examples={
            "1": {
                "summary": "Валидный запрос", 
                "value": {"title": "Mocsow Plaza", "location": "Mocsow"}
            }
        }
    )
) -> dict:
    async with async_session_maker() as session:
        add_hotel_stmt = insert(HotelsORM).values(**hotel.model_dump())
        await session.execute(add_hotel_stmt)
        await session.commit()
    return {"status": "ok"}


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
