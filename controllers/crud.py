from sqlalchemy.orm import Session


def get(
        model,
        db: Session,
        skip: int = 0,
        limit: int = 100
):
    return db.query(model).offset(skip).limit(limit).all()


def create(peternak, db: Session):
    db.add(peternak)
    db.commit()
    db.refresh(peternak)
    return peternak


def get_by_id(model, id: int, db: Session):
    return db.query(model).filter(
        model.id == id
    ).first()


def remove(model, peternak, db: Session):
    db.delete(peternak)
    db.commit()
    return get(model, db)
