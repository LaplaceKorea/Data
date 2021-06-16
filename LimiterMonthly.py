
from datetime import timedelta
from Limiter import *
from utils import add_one_month

class LimiterMonthly(Limiter):
    def __init__(self, n: int):
        self.t0: datetime = datetime.now()
        self.t01m = add_one_month(self.t0)
        self.n: int = n
        self.last: datetime = self.t0
        self.count: int = 0
    def canDo(self, context: "Dict[str,Any]", t: datetime) -> bool:
        tlimit = self.t0 + (self.t01m - self.t0) * float(self.count+1) / float(self.n)
        print("[monthly] canDo?", self.t0, tlimit, t)
        return t > tlimit
    def recordDo(self, context: "Dict[str,Any]", t: datetime):
        self.count = self.count + 1
        self.last = t

registerLimiterbuilder("Monthly", lambda x: LimiterMonthly(x["queriesPerMonth"]))
