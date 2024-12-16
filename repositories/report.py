from controllers.crud import Crud
from sqlalchemy.sql.expression import func


class Report(Crud):
    def range_report(self, since, until):
        return self.db.query(
            self.model.juleha_id, func.count(self.model.waktu_sembelih)
        ).filter(self.model.waktu_sembelih.between(since, until)).all()
