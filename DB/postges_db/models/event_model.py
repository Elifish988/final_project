from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from DB.postges_db.db import Base
from DB.postges_db.models.date_model import EventDate
from DB.postges_db.models.location_model import Location
from DB.postges_db.models.attack_model import Attack
from DB.postges_db.models.target_model import Target
from DB.postges_db.models.gname_model import Gname


class Event(Base):
    __tablename__ = 'event'

    id = Column(Integer, primary_key=True)
    date_id = Column(Integer, ForeignKey('date.id'))
    location_id = Column(Integer, ForeignKey('location.id'))
    attack_id = Column(Integer, ForeignKey('attack.id'))
    target_id = Column(Integer, ForeignKey('target.id'))
    gname_id = Column(Integer, ForeignKey('gname.id'))

    nkill = Column(Float, nullable=True)
    nwound = Column(Float, nullable=True)
    nperps = Column(Float, nullable=True)

    date = relationship("EventDate", back_populates="event", uselist=False)
    location = relationship("Location", back_populates="event", uselist=False)
    attack = relationship("Attack", back_populates="events")
    target = relationship("Target", back_populates="events")
    gname = relationship("Gname", back_populates="events")
