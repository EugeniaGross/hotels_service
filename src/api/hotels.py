from typing import Annotated

from fastapi import APIRouter, Query, Body, Depends, status, HTTPException
from sqlalchemy import insert, select, delete

from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.models.hotels import HotelsORM
from src.repositories.hotels import HotelRepository
from src.schemas.hotels import Hotel, HotelPATCH

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
async def get_hotels(
    pagination: PaginationDep,
    location: str | None = Query(default=None, description="Адрес отеля"),
    title: str | None = Query(default=None, description="Название отеля"),
) -> list[Hotel]:
    async with async_session_maker() as session:
        hotels = await HotelRepository(session).get_all(
            location, 
            title, 
            limit=pagination.per_page, 
            offset=(pagination.page - 1) * pagination.per_page
        )
    return hotels


@router.delete("/{hotel_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_hotel(hotel_id: int) -> None:
    async with async_session_maker() as session:
        hotel = await HotelRepository(session).delete(
            id=hotel_id
        )
        await session.commit()
        hotel = hotel.scalar_one_or_none()
    if hotel is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
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
):
    async with async_session_maker() as session:
        hotel = await HotelRepository(session).add(
            hotel
        )
        await session.commit()
    return {"status": "ok", "data": hotel.scalar_one_or_none()}


@router.put("/{hotel_id}")
async def update_hotel(
    hotel_id: int,
    hotel: Hotel
):
    async with async_session_maker() as session:
        hotel = await HotelRepository(session).edit(
            hotel,
            id=hotel_id
        )
        await session.commit()
        hotel = hotel.scalar_one_or_none()
    if hotel is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return {"status": "ok", "data": hotel}


@router.patch("/{hotel_id}")
async def partial_update_hotel(
    hotel_id: int,
    hotel: HotelPATCH
):
    async with async_session_maker() as session:
        hotel = await HotelRepository(session).edit(
            hotel,
            id=hotel_id
        )
        await session.commit()
        hotel = hotel.scalar_one_or_none()
    if hotel is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return {"status": "ok", "data": hotel}
