from typing import Generator
from sqlalchemy.orm import Session
from db import SessionLocal
import os
from fastapi import Header, HTTPException, status

def api_key_auth(x_api_key: str = Header(default="")) -> None:
    expected = os.getenv("API_KEY", "dev-key")
    if not expected or x_api_key != expected:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
