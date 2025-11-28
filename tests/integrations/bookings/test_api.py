import pytest


@pytest.mark.parametrize(
    "room_id, date_from, date_to, status_code",
    [
        (1, "2024-08-01", "2024-08-10", 201),
        (1, "2024-08-02", "2024-08-11", 201),
        (1, "2024-08-03", "2024-08-12", 201),
        (1, "2024-08-04", "2024-08-13", 201),
        (1, "2024-08-05", "2024-08-14", 201),
        (1, "2024-08-06", "2024-08-15", 500),
        (1, "2024-08-17", "2024-08-25", 201),
    ],
)
async def test_add_booking(
    room_id, date_from, date_to, status_code, db, authenticated_ac
):
    response = await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        },
    )
    assert response.status_code == status_code
    if status_code == 200:
        res = response.json()
        assert isinstance(res, dict)
        assert res["status"] == "OK"
        assert "data" in res


@pytest.mark.parametrize(
    "room_id, date_from, date_to, status_code, count",
    [
        (1, "2024-08-01", "2024-08-10", 200, 1),
        (1, "2024-08-02", "2024-08-11", 200, 2),
        (1, "2024-08-03", "2024-08-12", 200, 3),
    ],
)
async def test_add_and_get_my_bookings(
    room_id, date_from, date_to, status_code, count, del_bookings, authenticated_ac
):
    await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        },
    )
    response_2 = await authenticated_ac.get("/bookings/me")
    assert len(response_2.json()) == count
    assert response_2.status_code == status_code
