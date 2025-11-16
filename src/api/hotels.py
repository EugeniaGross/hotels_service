from datetime import date

from fastapi import APIRouter, Query, Body, status, HTTPException
from fastapi_cache.decorator import cache

from src.api.dependencies import PaginationDep, DBDep
from src.schemas.hotels import Hotel, HotelPATCH

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
@cache(expire=60)
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    date_from: date,
    date_to: date,
    location: str | None = Query(default=None, description="Адрес отеля"),
    title: str | None = Query(default=None, description="Название отеля"),
) -> list[Hotel]:
    hotels = await db.hotels.get_filtered_by_time(
        date_from=date_from,
        date_to=date_to,
        location=location, 
        title=title, 
        limit=pagination.per_page, 
        offset=(pagination.page - 1) * pagination.per_page
    )
    return hotels


@router.get("/{hotel_id}")
async def get_hotel(hotel_id: int, db: DBDep,) -> Hotel | None:
    hotel = await db.hotels.get_one_or_none(
        id=hotel_id
    )
    if hotel is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return {"status": "ok", "data": hotel} 


@router.delete("/{hotel_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_hotel(hotel_id: int, db: DBDep,) -> None:
    hotel = await db.hotels.delete(
        id=hotel_id
    )
    await db.commit()
    if hotel is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return 


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_hotel(
    db: DBDep,
    data: Hotel = Body(
        openapi_examples={
            "1": {
                "summary": "Валидный запрос", 
                "value": {"title": "Mocsow Plaza", "location": "Mocsow"}
            }
        }
    ),
) -> Hotel:
    hotel = await db.hotels.add(
        data
    )
    await db.commit()
    return {"status": "ok", "data": hotel}


@router.put("/{hotel_id}")
async def update_hotel(
    db: DBDep,
    hotel_id: int,
    hotel: Hotel
) -> Hotel:
    hotel = await db.hotels.edit(
        hotel,
        id=hotel_id
    )
    await db.commit()
    if hotel is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return {"status": "ok", "data": hotel}


@router.patch("/{hotel_id}")
async def partial_update_hotel(
    db: DBDep,
    hotel_id: int,
    hotel: HotelPATCH
) -> Hotel:
    hotel = await db.hotels.edit(
        hotel,
        id=hotel_id
    )
    await db.commit()
    if hotel is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return {"status": "ok", "data": hotel}
