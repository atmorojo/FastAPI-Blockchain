from controllers.crud import Crud
from sqlalchemy.sql.expression import func


class Report(Crud):
    def range_report(self, since, until):
        return self.db.query(
            self.model.juleha_id, func.count(self.model.waktu_sembelih)
        ).filter(self.model.waktu_sembelih.between(since, until))

    def group_by_juleha(self, query):
        return query.group_by(self.model.juleha_id)

    def group_by_penyelia(self, query):
        return query.group_by(self.model.penyelia_id)
