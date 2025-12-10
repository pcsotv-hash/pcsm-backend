from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import os

from fastapi_app.deps import get_db, api_key_auth
from models.member import Member
from fastapi_app.utils.qr_utils import generate_qr
from fastapi_app.utils.pdf_utils import generate_member_card

router = APIRouter(prefix="/api/admin", tags=["Admin"])


@router.put("/approve/{member_id}", dependencies=[Depends(api_key_auth)])
def approve_member(member_id: str, db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.membership_id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    member.status = "approved"

    # Ensure QR exists
    if not member.qr_code or not os.path.isfile(member.qr_code):
        member.qr_code = generate_qr(member.membership_id)

    # Generate PDF card
    pdf_path = generate_member_card(member)
    member.card_pdf = pdf_path

    db.commit()
    db.refresh(member)

    return {"status": 1, "pdf": pdf_path, "qr": member.qr_code}