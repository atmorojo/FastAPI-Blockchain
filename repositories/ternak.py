from controllers.crud import Crud
import src.models as models
import sqlalchemy


class Ternak_Repo(Crud):
    def __init__(self, db):
        super().__init__(models.Ternak, db)

    def get_by_date(self, field, sejak, sampai):
        """
        TODO:
        - Add offset
        - Add limit
        """
        return (
            self.db.query(self.model)
            .filter(
                sqlalchemy.or_(
                    self.model.waktu_sembelih.is_(None),
                    getattr(self.model, field).between(sejak, sampai),
                )
            )
            .all()
        )
