from sqlalchemy import Column, Integer, String
from DB.postges_db.db import Base
from sqlalchemy.orm import relationship


class Attack(Base):
    __tablename__ = 'attack'

    id = Column(Integer, primary_key=True)
    attacktype1 = Column(Integer)
    attacktype1_txt = Column(String)

    events = relationship("Event", back_populates="attack")

