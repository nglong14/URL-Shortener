from .. import models, schemas, utils, oauth2
from fastapi import FastAPI, Response, HTTPException, Depends, APIRouter, status
from ..database import get_db, SessionLocal
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(
    prefix="/interviews",
    tags=['Interviews']
)

# Get all interviews for the current user
@router.get("/", response_model=List[schemas.InterviewResponse])
def get_interviews(db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not validate credentials")
    interviews = db.query(models.Interview).filter(models.Interview.user_id == current_user.id).all()
    return interviews

# Get a specific interview by ID
@router.get("/{id}", response_model=schemas.InterviewResponse)
def get_interview(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not validate credentials")
    interview = db.query(models.Interview).filter(
        models.Interview.id == id,
        models.Interview.user_id == current_user.id
    ).first()
    if not interview:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Interview not found")
    return interview

# Create interview
@router.post("/", response_model=schemas.InterviewResponse, status_code=status.HTTP_201_CREATED)
def create_interview(interview: schemas.InterviewCreate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not validate credentials")
    db_interview = models.Interview(
        **interview.dict(),
        user_id=current_user.id
    )
    db.add(db_interview)
    db.commit()
    db.refresh(db_interview)
    return db_interview