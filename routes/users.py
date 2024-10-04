from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from controllers import user_ctrl
from src import models, schemas
from src.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

routes = APIRouter(
    prefix="/users"
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@routes.post("/", response_model=schemas.User)
def create_user(
        user: schemas.UserCreate,
        db: Session = Depends(get_db)
):
    print(db)
    db_user = user_ctrl.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_ctrl.create_user(db=db, user=user)


@routes.get("/", response_model=list[schemas.User])
def read_users(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
):
    users = user_ctrl.get_users(db, skip=skip, limit=limit)
    return users


@routes.get("/{user_id}", response_model=schemas.User)
def read_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    db_user = user_ctrl.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
