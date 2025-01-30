from src import models
from controllers.crud import Crud
import hashlib


class UserCrud(Crud):
    def __init__(self, db):
        self.db = db
        self.model = models.User

    def get_user(self, user_id: int):
        return self.db.query(self.model).filter(models.User.id == user_id).first()

    def get_user_by_username(self, username: str):
        return (
            self.db.query(self.model).filter(models.User.username == username).first()
        )

    def get_user_by_email(self, email: str):
        return self.db.query(self.model).filter(models.User.email == email).first()

    def get_users(self, skip: int = 0, limit: int = 100, sadmin=False):
        if not sadmin:
            result = (
                self.db.query(self.model)
                .join(models.Role, models.Role.user_id == models.User.id)
                .filter(models.Role.role != 0)
                .offset(skip)
                .limit(limit)
                .all()
            )
        else:
            result = self.db.query(self.model).offset(skip).limit(limit).all()
        return result

    def create_user(self, user):
        hashed_password = hashlib.sha256(user.password.encode()).hexdigest()
        user.password = hashed_password
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
