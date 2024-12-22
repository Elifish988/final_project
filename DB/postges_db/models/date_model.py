from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship
from DB.postges_db.db import Base

class EventDate(Base):
    __tablename__ = 'date'

    id = Column(Integer, primary_key=True)
    iyear = Column(Integer, nullable=True)
    imonth = Column(Integer, nullable=True)
    iday = Column(Integer, nullable=True)

    event = relationship("Event", back_populates="date")
