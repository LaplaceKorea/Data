
from typing import List
from Fetcher import *

class FetchersOneLimit(Fetcher):
    def __init__(self, fetchers: List[Fetcher]):
        self.fetchers = fetchers
        self.select = -1
    def setLimiter(self, l: Limiter):
        self.limiter = l
        for i in range(len(self.fetchers)):
            self.fetchers[i].setLimiter(l)
    def tryFetch(self) -> bool:
        for i in range(len(self.fetchers)):
            idx = (i+self.select+1) % len(self.fetchers)
            print("try idx=", idx)
            if self.fetchers[idx].tryFetch():
                self.select = idx
                return True
        return False
    def fetch(self):
        return self.fetchers[self.select].fetch()

def FetchersOneLimitBuilder(cfg: Dict[str,Any]) -> Fetcher:
    fetchers: List[Fetcher] = []
    for i in range(len(cfg["fetchers"])):
        f = fetcherBuilder(cfg["fetchers"][i])
        fetchers.append(f)
    return FetchersOneLimit(fetchers)

registerFetcherBuilder("OneLimit", FetchersOneLimitBuilder)
