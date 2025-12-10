from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi_app.deps import get_db, api_key_auth
from models.member import Member
from fastapi_app.utils.qr_utils import generate_qr
from fastapi_app.schemas import MemberCreate, MemberOut

router = APIRouter(prefix="/members", tags=["Members"])


@router.post("/register", response_model=MemberOut, dependencies=[Depends(api_key_auth)])
def register_member(member_data: MemberCreate, db: Session = Depends(get_db)) -> MemberOut:

    # Check duplicate CNIC
    existing = db.query(Member).filter(Member.cnic == member_data.cnic).first()
    if existing:
        raise HTTPException(status_code=400, detail="CNIC already registered")

    # Auto Membership ID
    membership_id = f"PCSM-{member_data.cnic[-4:]}"

    # Generate QR Code file
    qr_url = generate_qr(membership_id)

    # Save Member
    member = Member(
        full_name=member_data.full_name,
        father_name=member_data.father_name,
        cnic=member_data.cnic,
        phone=member_data.phone,
        membership_id=membership_id,
        qr_code=qr_url,
        city=member_data.city,
        district=member_data.district,
        designation=member_data.designation,
        membership_type=member_data.membership_type,
    )

    db.add(member)
    db.commit()
    db.refresh(member)

    return member
