
from datetime import datetime, timedelta
from typing import Dict, Callable, Any, List, Tuple
import numpy as np

class Features:
    def getDescription(self)->List[Tuple[str,Dict[str,Any]]]:
        pass
    def getFeatureSize(self) -> int:
        pass
    def getFeature(self, fromDT: datetime, toDT: datetime, timestep: timedelta) -> np.ndarray:
        pass

featureBuilders: "Dict[str,Callable[[Dict[str,Any]],Features]]" = {}

def registerFeatureBuilder(name: str, builder: "Callable[[Dict[str,Any]],Features]"):
    featureBuilders[name] = builder

def featureBuilder(config: "Dict[str,Any]") -> Features:
    return featureBuilders[config["features"]](config)
