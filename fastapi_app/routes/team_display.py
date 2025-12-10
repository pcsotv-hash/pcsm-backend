from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.team_display import TeamDisplay
from models.member import Member
from fastapi_app.deps import get_db, api_key_auth
from fastapi_app.schemas import TeamDisplayCreate, TeamDisplayOut

router = APIRouter(prefix="/team", tags=["Team Display"])

# Add Member to Team
@router.post("/", response_model=TeamDisplayOut, dependencies=[Depends(api_key_auth)])
def add_to_team(data: TeamDisplayCreate, db: Session = Depends(get_db)) -> TeamDisplayOut:
    member = db.query(Member).filter(Member.id == data.member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    entry = TeamDisplay(**data.model_dump())
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry

# List Team Display in Order
@router.get("/", response_model=list[TeamDisplayOut])
def list_team(db: Session = Depends(get_db)) -> list[TeamDisplayOut]:
    return db.query(TeamDisplay).order_by(TeamDisplay.order_number).all()

# Update order or visibility
@router.put("/{team_id}", response_model=TeamDisplayOut, dependencies=[Depends(api_key_auth)])
def update_team(team_id: int, data: TeamDisplayCreate, db: Session = Depends(get_db)) -> TeamDisplayOut:
    team = db.query(TeamDisplay).filter(TeamDisplay.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team entry not found")

    for key, value in data.model_dump().items():
        setattr(team, key, value)

    db.commit()
    db.refresh(team)
    return team
