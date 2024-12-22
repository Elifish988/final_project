from sqlalchemy import Column, Integer, String
from DB.postges_db.db import Base
from sqlalchemy.orm import relationship


class Target(Base):
    __tablename__ = 'target'

    id = Column(Integer, primary_key=True)
    targetype1 = Column(Integer)
    targetype1_txt = Column(String)

    events = relationship("Event", back_populates="target")