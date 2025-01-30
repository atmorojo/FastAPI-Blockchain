from controllers.crud import Crud
from src import models


class Penyelia_Repo(Crud):
    def __init__(self, db):
        super().__init__(models.Penyelia, db)

    def get_rph_filtered(self, rph_id):
        return (
            self.db.query(self.model, models.User, models.Role)
            .join(models.Role, models.Role.user_id == models.User.id)
            .join(self.model, models.Role.acting_as == self.model.id)
            .filter(self.model.rph_id == rph_id)
            .all()
        )
