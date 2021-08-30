from sqlalchemy import Column, Integer, FLOAT, String
from services.database import Base


class Trips(Base):
    __tablename__ = "trips"

    Route = Column(String, primary_key=True, index=True)
    Origin = Column(String, index=True)
    Destination = Column(String, index=True)
    WeeklyCapacity = Column(Integer)