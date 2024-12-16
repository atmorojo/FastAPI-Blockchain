from controllers.crud import Crud


class Report(Crud):
    def range_report(self):
        return self.db.query(
            self.model.juleha_id, func.count(self.model.waktu_sembelih)
        ).filter(getattr(self.model, date_field).between(sejak, sampai))
