from fastapi import FastAPI, Query, Body
import uvicorn

app = FastAPI()

hotels = [
    {"id": 1, "title": "Dubai", "name": "dubai"},
    {"id": 2, "title": "Sochi", "name": "sochi"},
]


@app.get("/hotels")
def get_hotels(
    id: int | None = Query(default=None, description="ID отеля"),
    title: str | None = Query(default=None, description="Название отеля")
):
    global hotels
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    return hotels_


@app.delete("/hotels/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "Ok"}   


@app.post("/hotels")
def create_hotel(
    title: str = Body(description="Название отеля"),
    name: str = Body(description="Слаг отеля")
):
    global hotels
    new_hotel = {"id": hotels[-1]["id"] + 1, "title": title, "name": name}
    hotels.append(new_hotel)
    return new_hotel


@app.put("/hotels/{hotel_id}")
def update_hotel(
    hotel_id: int,
    title: str = Body(description="Название отеля"),
    name: str = Body(description="Слаг отеля")
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = title
            hotel["name"] = name
            return hotel
    return {"error": f"Отеля с id={hotel_id} не существует"}


@app.patch("/hotels/{hotel_id}")
def partial_update_hotel(
    hotel_id: int,
    title: str | None = Body(default=None, embed=True, description="Название отеля"),
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = title if title is not None else hotel["title"]
            return hotel
    return {"error": f"Отеля с id={hotel_id} не существует"}


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True, port=7000)
    