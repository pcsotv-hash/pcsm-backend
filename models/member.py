from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from db import Base


class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)
    membership_id = Column(String, unique=True, index=True)
    full_name = Column(String, nullable=False)
    father_name = Column(String, nullable=True)
    cnic = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=True)
    qr_code = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    city = Column(String, nullable=True)
    district = Column(String, nullable=True)
    designation = Column(String, nullable=True)
    membership_type = Column(String, nullable=True)
    district_id = Column(Integer, nullable=True)
    tehsil_id = Column(Integer, nullable=True)
    password = Column(String, nullable=True)
    status = Column(String, default="pending")
    card_pdf = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
