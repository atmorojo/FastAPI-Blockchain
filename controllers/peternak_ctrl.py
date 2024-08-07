from sqlalchemy.orm import Session

from src import models


def get_peternaks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Peternak).offset(skip).limit(limit).all()


def create_peternak(db: Session, peternak: models.Peternak):
    db.add(peternak)
    db.commit()
    db.refresh(peternak)
    return peternak


def get_peternak(db: Session, peternak_id: int):
    return db.query(models.Peternak).filter(
        models.Peternak.id == peternak_id
    ).first()


def rm_peternak(db: Session, peternak: models.Peternak):
    db.delete(peternak)
    db.commit()
    return get_peternaks(db)
