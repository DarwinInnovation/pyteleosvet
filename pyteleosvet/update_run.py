from pyteleosvet.model import *
import datetime

class FakeUpdateRun(object):
    def __init__(self, ur):
        self.datetime = ur._fake_dt
        self.type = ur.type

class UpdateRun():
    def __init__(self, type):
        self.type = type
        self._mark = None
        self._fake_dt = datetime.datetime(2000, 1, 1)

    def get_latest(self):
        try:
            self.latest = UpdateRunModel. \
                select().where(UpdateRunModel.type == self.type).order_by(UpdateRunModel.datetime.desc()).get()
        except:
            self.latest = FakeUpdateRun(self)

        return self.latest.datetime

    def mark(self):
        self._mark = datetime.datetime.today()
        return self._mark

    def write(self):
        if self._mark is None:
            raise ValueError('Update not marked')

        UpdateRunModel.create(datetime=self._mark, type=self.type)

