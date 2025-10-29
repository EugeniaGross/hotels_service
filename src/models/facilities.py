from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class FacilitiesORM(Base):
    __tablename__ = "facilities"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    
    rooms: Mapped[list["RoomsORM"]] = relationship(
        secondary="rooms_facilities",
        back_populates="facilities"
    )
    
    
class RoomsFacilitiesORM(Base):
    __tablename__ = "rooms_facilities"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    facility_id: Mapped[int] = mapped_column(ForeignKey("facilities.id"))
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
