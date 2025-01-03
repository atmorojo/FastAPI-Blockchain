from controllers.crud import Crud
from sqlalchemy.sql.expression import func


class Report(Crud):
    def __init__(self, db, ternak, transaksi):
        super().__init__(ternak, db)
        self.trans = transaksi

    def ternak_range_report(self, since, until):
        self.query = self.db.query(
            self.model, func.count(self.model.waktu_sembelih)
        ).filter(self.model.waktu_sembelih.between(since, until))
        return self

    def kiriman_range_report(self, since, until):
        self.query = self.db.query(
            self.trans, func.count(self.trans.waktu_kirim)
        ).filter(self.trans.waktu_kirim.between(since, until))
        return self

    def group_by_juleha(self):
        self.query = self.query.group_by(self.model.juleha_id)
        return self

    def group_by_lapak(self):
        self.query = self.query.group_by(self.trans.lapak_id)
        return self

    def group_by_peternak(self):
        self.query = self.query.group_by(self.model.peternak)
        return self

    def group_by_date(self):
        self.query = self.query.group_by(self.model.waktu_sembelih)
        return self

    def group_by_waktu_kirim(self):
        self.query = self.query.group_by(self.trans.waktu_kirim)
        return self

    def get_all(self):
        return self.query.all()
