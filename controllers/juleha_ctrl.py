from sqlalchemy.orm import Session

from src import models


def get_julehas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Juleha).offset(skip).limit(limit).all()


def create_juleha(db: Session, juleha: models.Juleha):
    db.add(juleha)
    db.commit()
    db.refresh(juleha)
    return juleha


def get_juleha(db: Session, juleha_id: int):
    return db.query(models.Juleha).filter(models.Juleha.id == juleha_id).first()


def rm_juleha(db: Session, juleha: models.Juleha):
    db.delete(juleha)
    db.commit()
    return get_julehas(db)
