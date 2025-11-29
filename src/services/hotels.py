from datetime import date
from src.exceptions import ObjectNotFoundException, check_date_to_after_date_from
from src.schemas.hotels import Hotel, HotelPATCH
from src.services.base import BaseService


class HotelService(BaseService):
    async def get_hotels(
        self, 
        date_from: date,
        date_to: date,
        location: str,
        title: str,
        limit: int,
        offset: int
    ):
        check_date_to_after_date_from(date_from, date_to)
        hotels = await self.db.hotels.get_filtered_by_time(
            date_from=date_from,
            date_to=date_to,
            location=location,
            title=title,
            limit=limit,
            offset=offset,
        )
        return hotels
    
    async def get_hotel(self, hotel_id: int):
        hotel = await self.db.hotels.get_one_or_none(id=hotel_id)
        if not hotel:
            raise ObjectNotFoundException
        return hotel
    
    async def delete_hotel(self, hotel_id: int):
        hotel = await self.db.hotels.delete(id=hotel_id)
        await self.db.commit()
        if hotel is None:
            raise ObjectNotFoundException
        
    async def create_hotel(self, data: Hotel):
        hotel = await self.db.hotels.add(data)
        await self.db.commit()
        return hotel
    
    async def update_hotel(self, hotel_id: int, hotel: Hotel, exclude_unset: bool) -> dict:
        hotel = await self.db.hotels.edit(hotel, id=hotel_id, exclude_unset=False)
        await self.db.commit()
        if hotel is None:
            raise ObjectNotFoundException
        return hotel
    
    async def partial_update_hotel(self, hotel_id: int, hotel: HotelPATCH) -> dict:
        hotel = await self.db.hotels.edit(hotel, id=hotel_id, exclude_unset=True)
        await self.db.commit()
        if hotel is None:
            raise ObjectNotFoundException
        return hotel