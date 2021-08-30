from sqlalchemy import Column, Integer, FLOAT, String
from services.database import Base


class Locations(Base):
    __tablename__ = "locations"

    LocationCode = Column(String, primary_key=True, index=True)
    Latitude = Column(FLOAT)
    Longitude = Column(FLOAT)
    FacilityOwnedByCarvana = Column(Integer)