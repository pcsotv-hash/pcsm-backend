import qrcode
import os
from datetime import datetime, timezone
from typing import Final

STATIC_ROOT: Final[str] = os.path.join("fastapi_app", "static")
QR_FOLDER: Final[str] = os.path.join(STATIC_ROOT, "qrs")

# Ensure QR folder exists
os.makedirs(QR_FOLDER, exist_ok=True)

def generate_qr(membership_id: str) -> str:
    """Generate a QR PNG for the given membership_id and return file path."""
    qr_data = f"https://pcsm.com/member/{membership_id}"
    filename = f"{membership_id}_{datetime.now(timezone.utc).timestamp()}.png"
    filepath = os.path.join(QR_FOLDER, filename)

    qr = qrcode.make(qr_data)
    qr.save(filepath)

    return filepath
