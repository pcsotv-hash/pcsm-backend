from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import os

from fastapi_app.deps import get_db
from models.member import Member
from fastapi_app.utils.pdf_utils import generate_member_card

router = APIRouter()   # ✅ THIS WAS MISSING


@router.get("/card/{member_id}")
def download_card(member_id: str, db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    # Agar PDF pehle se nahi bani, generate karo
    if not member.card_pdf or not os.path.exists(member.card_pdf):
        pdf_path = generate_member_card(member)
        member.card_pdf = pdf_path
        db.commit()
    else:
        pdf_path = member.card_pdf

    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename=os.path.basename(pdf_path)
    )
