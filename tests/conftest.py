import json
from unittest import mock

mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f).start()

from httpx import AsyncClient
import pytest

from src.config import settings
from src.database import Base, engine_null_pool
from src.models import *
from src.main import app
from src.schemas.hotels import HotelAdd
from src.schemas.rooms import RoomAdd
from src.utils.db_manager import DBManager
from src.database import async_session_maker_null_pool
from src.api.dependencies import get_db


@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    async with DBManager(session_factory=async_session_maker_null_pool) as db_:
        with open("tests/mock_hotels.json", encoding="utf-8") as hotels_json:
            hotels_data = [HotelAdd(**data) for data in json.load(hotels_json)]
            await db_.hotels.add_bulk(hotels_data)
        with open("tests/mock_rooms.json", encoding="utf-8") as rooms_json:
            rooms_data = [RoomAdd(**data) for data in json.load(rooms_json)]
            await db_.rooms.add_bulk(rooms_data) 
        await db_.commit() 
        
        
async def get_db_null_pool():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db 
        
        
@pytest.fixture(scope="function")
async def db():
    async for db in get_db_null_pool():
        yield db
        
        
@pytest.fixture(scope="module")
async def del_bookings():
    async for db_ in get_db_null_pool():
        await db_.bookings.delete_bulk()
        await db_.commit()
        
        
app.dependency_overrides[get_db] = get_db_null_pool


@pytest.fixture(scope="session")
async def ac():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
        
        
@pytest.fixture(scope="session", autouse=True)
async def register_user(setup_database, ac):
    await ac.post(
        "/auth/register",
        json={
            "email": "kot@pes.com",
            "password": "1234"
        }
    )
    
    
@pytest.fixture(scope="session")
async def authenticated_ac(register_user, ac):
    await ac.post(
        "/auth/login",
        json={
            "email": "kot@pes.com",
            "password": "1234"
        }
    )
    assert ac.cookies["access_token"]
    yield ac
        