from src.schemas.hotels import HotelAdd


async def test_add_hotel(db):
    data = HotelAdd(title="Отель", location="Москва")
    hotel = await db.hotels.add(data)
    await db.commit()