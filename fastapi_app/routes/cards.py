import os
import zipfile
from pathlib import Path
from typing import List

from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse

from fastapi_app.utils.pdf_utils import generate_member_card, CARDS_DIR

router = APIRouter(prefix="/cards", tags=["Membership Cards"])

# --- MOCK DATABASE (Updated with fields from Image) ---
def get_member_by_id(membership_id: str):
    # In production, fetch this from DB
    return {
        "membership_id": membership_id,
        "name": "Muhammad Ismail",
        "father_name": "Noor Hamid Jan",
        "cnic": "152303-9974536-3",
        "designation": "Deputy General Secretary",
        "expiry_date": "Oct-2026",
        "photo_path": "fastapi_app/static/uploads/dummy_user.jpg" 
    }

def get_all_member_ids():
    return ["1001", "1002"]

# --- ENDPOINTS ---

@router.post("/generate/{membership_id}")
async def trigger_card_generation(membership_id: str, background_tasks: BackgroundTasks):
    member = get_member_by_id(membership_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    
    background_tasks.add_task(generate_member_card, member)
    return {"status": "processing", "message": f"Card generation started for {membership_id}"}

@router.get("/download/{membership_id}")
async def download_card(membership_id: str):
    pdf_path = CARDS_DIR / f"{membership_id}.pdf"
    
    if not pdf_path.exists():
        member = get_member_by_id(membership_id)
        if not member:
            raise HTTPException(status_code=404, detail="Member not found")
        generate_member_card(member)
            
    return FileResponse(
        path=pdf_path, 
        filename=f"Card_{membership_id}.pdf", 
        media_type='application/pdf'
    )

@router.get("/download-bulk/zip")
async def download_all_cards_zip():
    zip_path = CARDS_DIR / "all_cards.zip"
    member_ids = get_all_member_ids()
    
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for m_id in member_ids:
            pdf_file = CARDS_DIR / f"{m_id}.pdf"
            if pdf_file.exists():
                zipf.write(pdf_file, arcname=f"{m_id}.pdf")
    
    if not zip_path.exists():
        raise HTTPException(status_code=404, detail="No cards generated yet")
        
    return FileResponse(path=zip_path, filename="Membership_Cards.zip", media_type='application/zip')