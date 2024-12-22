from sqlalchemy import Column, Integer, Float, String
from DB.postges_db.db import Base
from sqlalchemy.orm import relationship


class Location(Base):
    __tablename__ = 'location'
    id = Column(Integer, primary_key=True)
    region = Column(Integer, nullable=True)
    region_txt = Column(String, nullable=True)
    country = Column(Integer, nullable=True)
    country_txt = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    event = relationship("Event", back_populates="location")





