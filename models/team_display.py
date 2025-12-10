from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from db import Base

class TeamDisplay(Base):
    __tablename__ = "team_display"

    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("members.id", ondelete="CASCADE"))
    position_title = Column(String)
    order_number = Column(Integer, default=999)
    visible = Column(Boolean, default=True)