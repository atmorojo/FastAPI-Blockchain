from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from controllers import user_ctrl
from src import models, schemas
from src.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

routes = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@routes.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = user_ctrl.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_ctrl.create_user(db=db, user=user)


@routes.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = user_ctrl.get_users(db, skip=skip, limit=limit)
    return users


@routes.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_ctrl.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@routes.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return user_ctrl.create_user_item(db=db, item=item, user_id=user_id)


@routes.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = user_ctrl.get_items(db, skip=skip, limit=limit)
    return items