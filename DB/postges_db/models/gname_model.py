from sqlalchemy import Column, Integer, String
from DB.postges_db.db import Base
from sqlalchemy.orm import relationship


class Gname(Base):
    __tablename__ = 'gname'

    id = Column(Integer, primary_key=True)
    gname = Column(String)

    events = relationship("Event", back_populates="gname")