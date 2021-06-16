
from typing import Any, Callable, Dict
from datetime import datetime

class Limiter:
    def canDo(self, context: "Dict[str,Any]", t: datetime) -> bool:
        pass
    def recordDo(self, context: "Dict[str,Any]", t: datetime):
        pass

limiterBuilders: "Dict[str,Callable[[Dict[str,Any]],Limiter]]" = {}

def registerLimiterbuilder(name: str, builder: "Callable[[Dict[str,Any]],Limiter]"):
    global limiterBuilder
    limiterBuilders[name] = builder

def limiterBuilder(config: "Dict[str,Any]") -> Limiter:
    return limiterBuilders[config["limiter"]](config)

registerLimiterbuilder("None", lambda x: Limiter())
