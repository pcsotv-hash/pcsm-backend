from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi_app.deps import get_db
from models.member import Member
import base64
from fastapi_app.schemas import QRResponse

router = APIRouter(prefix="/qr", tags=["QR"])


@router.get("/{membership_id}", response_model=QRResponse)
def get_qr(membership_id: str, db: Session = Depends(get_db)) -> QRResponse:

    member = db.query(Member).filter(Member.membership_id == membership_id).first()

    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    if not member.qr_code:
        raise HTTPException(status_code=404, detail="QR not generated")

    # Read image file
    with open(member.qr_code, "rb") as f:
        qr_bytes = f.read()

    # Convert to base64
    qr_base64 = base64.b64encode(qr_bytes).decode("utf-8")

    return QRResponse(status="success", membership_id=membership_id, qr_base64=qr_base64)
