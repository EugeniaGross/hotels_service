from src.schemas.hotels import HotelAdd
from src.utils.db_manager import DBManager
from src.database import async_session_maker_null_pool


async def test_add_hotel():
    data = HotelAdd(title="Отель", location="Москва")
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        hotel = await db.hotels.add(data)
        await db.commit()