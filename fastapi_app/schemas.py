from pydantic import BaseModel, Field
from pydantic import ConfigDict
from typing import Annotated
from datetime import datetime

# ======================================================
# TEAM DISPLAY SCHEMAS (UPPER — because member uses none)
# ======================================================

class TeamDisplayBase(BaseModel):
    member_id: int
    position_title: Annotated[str, Field(min_length=1, max_length=100)]
    order_number: Annotated[int, Field(ge=0)] = 999
    visible: bool = True


class TeamDisplayCreate(TeamDisplayBase):
    model_config = ConfigDict(json_schema_extra={
        "examples": [{
            "member_id": 1,
            "position_title": "Lead",
            "order_number": 1,
            "visible": True
        }]
    })


class TeamDisplayOut(TeamDisplayBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# ======================================================
# MEMBER SCHEMAS
# ======================================================

class MemberBase(BaseModel):
    full_name: Annotated[str, Field(min_length=2, max_length=120)]
    father_name: str | None = None
    cnic: Annotated[str, Field(min_length=5, max_length=25)]
    phone: Annotated[str, Field(min_length=7, max_length=20)]
    membership_id: str | None = None
    qr_code: str | None = None
    image_url: str | None = None
    city: str | None = None
    district: str | None = None
    designation: str | None = None
    membership_type: str | None = None


class MemberCreate(MemberBase):
    model_config = ConfigDict(json_schema_extra={
        "examples": [{
            "full_name": "Test User",
            "father_name": "Parent",
            "cnic": "CNIC123456",
            "phone": "03001234567",
            "city": "City",
            "district": "District",
            "designation": "Member",
            "membership_type": "Standard"
        }]
    })


class MemberOut(MemberBase):
    id: int
    created_at: datetime
    updated_at: datetime | None

    model_config = ConfigDict(from_attributes=True)

class QRResponse(BaseModel):
    status: str
    membership_id: str
    qr_base64: str
