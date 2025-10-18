from pydantic import BaseModel, ConfigDict


class RoomAdd(BaseModel):
    title: str
    description: str
    price: str
    quantity: int
    
    
class Room(RoomAdd):
    id: int
    
    model_config = ConfigDict(from_attributes=True)
    
    
class RoomPATCH(BaseModel):
    title: str | None = None
    description: str | None = None
    price: str | None = None
    quantity: str | None = None
