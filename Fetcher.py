from typing import Dict, Callable, Any
from Limiter import Limiter, limiterBuilder

class Fetcher:
    def setLimiter(self, l: Limiter):
        pass
    def tryFetch(self) -> bool:
        pass
    def fetch(self):
        pass

fetchBuilders: Dict[str, Callable[[Dict[str,Any]],Fetcher]] = {}

def registerFetcherBuilder(name: str, builder: Callable[[Dict[str,Any]],Fetcher]):
    global fetchBuilders
    fetchBuilders[name] = builder

def fetcherBuilder(config: Dict[str,Any]) -> Fetcher:
    l = limiterBuilder(config)
    b = fetchBuilders[config["fetcher"]]
    r = b(config)
    r.setLimiter(l)
    return r

