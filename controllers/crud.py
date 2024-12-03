from sqlalchemy import desc

class Crud:
    def __init__(self, model, db):
        self.model = model
        self.db = db

    def get(self, skip: int = 0, limit: int = 100):
        return self.db.query(self.model).offset(skip).limit(limit).all()

    def get_by_date(self, field, sejak, sampai):
        return (
            self.db.query(self.model)
            .filter(getattr(self.model, field).between(sejak, sampai))
            .all()
        )

    def get_by_field_and_date(self, field, date_field, sejak, sampai):
        return (
            self.db.query(self.model)
            .filter(getattr(self.model, field) != null)
            .filter(getattr(self.model, date_field).between(sejak, sampai))
            .all()
        )

    def get_latest_field(self, field, date_field, date):
        return (
            self.db.query(self.model)
            .filter(getattr(self.model, date_field) == date)
            .order_by(desc(getattr(self.model, field)))
            .first()
        )

    def create(self, row):
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return row

    def get_by_id(self, id: int):
        return self.db.query(self.model).filter(self.model.id == id).first()

    def get_by(self, field: str, query):
        return (
            self.db.query(self.model)
            .filter(getattr(self.model, field) == query)
            .first()
        )

    def remove(self, row):
        self.db.delete(row)
        self.db.commit()
        return self.get()

    def update(self, row):
        self.db.commit()
        self.db.refresh(row)
        return row
