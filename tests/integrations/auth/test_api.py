import pytest


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("test@test.ru", "12345678", 200),
        ("test@test.ru", "12345678", 400),
        ("test", "12345678", 422),
    ],
)
async def test_registration(email, password, status_code, ac):
    response = await ac.post(
        "/auth/register", json={"email": email, "password": password}
    )
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "email, password, status_code",
    [("test@test.ru", "12345678", 200), ("test1@test.ru", "12345678", 401)],
)
async def test_login(email, password, status_code, ac):
    response = await ac.post("/auth/login", json={"email": email, "password": password})
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("test@test.ru", "12345678", 200),
    ],
)
async def test_auth_flow(email, password, status_code, ac):
    response = await ac.post("/auth/login", json={"email": email, "password": password})
    assert response.status_code == status_code
    assert response.cookies.get("access_token")
    response = await ac.get("/auth/me")
    assert response.status_code == status_code
    assert response.json()["email"] == email
    response = await ac.post("/auth/logout")
    assert response.status_code == status_code
