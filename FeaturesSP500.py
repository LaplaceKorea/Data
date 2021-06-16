
from typing import Any, Dict, List, Tuple
from Config import cfg
from Features import *
import numpy as np

DELAYED_BID = 66
DELAYED_ASK = 67
DELAYED_LAST = 68
DELAYED_BID_SIZE = 69
DELAYED_ASK_SIZE = 70
DELAYED_LAST_SIZE = 71
DELAYED_HIGH = 72
DELAYED_LOW = 73
DELAYED_VOLUME = 74
DELAYED_CLOSE = 75
DELAYED_OPEN = 76
TIMESTAMP = 88

translate = {
    DELAYED_BID: "DELAYED_BID",
    DELAYED_ASK: "DELAYED_ASK",
    DELAYED_LAST: "DELAYED_LAST",
    DELAYED_BID_SIZE: "DELAYED_BID_SIZE",
    DELAYED_ASK_SIZE: "DELAYED_ASK_SIZE",
    DELAYED_LAST_SIZE: "DELAYED_LAST_SIZE",
    DELAYED_HIGH: "DELAYED_HIGH",
    DELAYED_LOW: "DELAYED_LOW",
    DELAYED_VOLUME: "DELAYED_VOLUME",
    DELAYED_CLOSE: "DELAYED_CLOSE",
    DELAYED_OPEN: "DELAYED_OPEN",
    TIMESTAMP: "TIMESTAMP"
}

taboo = {
    "Symbol": True,
    "American Airlines Group": True,
    "0": True
}

stocks: Dict[str, int] = {
    # ex: "AAPL": 0, "ADBE":1
}

stockNames: Dict[str, str] = {}

import csv

ccount = 0
with open("constituents.csv") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row[0] in taboo:
            pass
        else:
            print(row[0], " => ", row[1])
            stocks[row[0]] = ccount
            stockNames[row[0]] = row[1]
            ccount = ccount+1

fields = {
    DELAYED_OPEN:0,
    DELAYED_HIGH:1,
    DELAYED_LOW:2,
    DELAYED_CLOSE:3
}

def loadSP500File(fn: str):
    raw_data: Dict[str,List[np.ndarray]] = {}

    # Z|#|field|size
    # P|#|field|price
    # S|#|type(88)|value(timestamp)

    # delayed-1623246971
    c = 1

    with open(fn) as infile:
        for line in infile:
            c = c + len(line)
            if line[0] == 'Z':
                pass
            if line[0] == 'P':
                elts = line.split("|")
                ticker = elts[1]
                if ticker in stocks:
                    field = int(elts[2])
                    price = float(elts[3])
                    if field in fields:
                        print(ticker, field, price)
                        if ticker in raw_data:
                            pass
                        else:
                            raw_data[ticker] = []                        
                        rd = raw_data[ticker]
                        try:
                            rd[len(rd)-1][fields[field]+1] = price
                        except:
                            pass
            if line[0] == 'S':
                elts = line.split("|")
                tickers = elts[1]
                if ticker in stocks:
                    field = int(elts[2])
                    ts = int(elts[3])
                    if field == TIMESTAMP:
                        print(ticker, "time=", ts)
                        if ticker in raw_data:
                            pass
                        else:
                            raw_data[ticker] = []
                        rd = raw_data[ticker]
                        a = np.zeros((len(fields)+1,), dtype=np.float32)
                        a[0] = ts
                        rd.append(a)
                
    # print(c) 
    # print(raw_data)

    finallist: List[np.ndarray] = []
    indices: Dict[str, int] = {}
    for k in stocks:
        indices[k] = 0
    ndone = 0
    farfuture = 1e37
    while ndone < len(indices):
        next = farfuture # whatever big
        selected = ""
        for k in indices:
            i = indices[k]
            try:
                d = raw_data[k]
                if i < len(d):
                    ts = d[i][0]
                    if ts < next:
                        next = ts
                        selected = k
            except:
                pass
        nextLine = np.zeros((len(stocks) * (len(fields)+1),), dtype=np.float32)
        # print(nextLine.shape)
        if selected == "":
            break
        for k in indices:
            i = indices[k]
            try:
                d = raw_data[k]
                if i < len(d):
                    ts = d[i][0]
                    if abs(ts-next) < 1e-12:
                        idx = stocks[k]
                        nextLine[(idx *(len(fields)+1)):(idx*(len(fields)+1)+(len(fields)+1))] = d[i][:]
                    indices[k] = i+1
            except:
                pass
        finallist.append(nextLine)

    f = np.vstack(finallist)
    print(f.shape)
    return f

# description
# List[Tuple[str,Dict[str,Any]]]
# feature size ~

featureSize = len(stocks) * (1 + len(fields))
print("featureSize=", featureSize)
featureDesc: List[Tuple[str,Dict[str,Any]]] = []

rstocks: Dict[int, str] = {}
rfields: Dict[int, int] = {}
for k in stocks:
    rstocks[stocks[k]] = k
for kk in fields:
    rfields[fields[kk]] = kk

ccount = 0
for i in range(len(stocks)):
    featureDesc.append((str(ccount), { "stock": rstocks[i], "field": "time"} ))
    ccount = ccount+1
    for j in range(len(fields)):
        featureDesc.append((str(ccount), { "stock": rstocks[i], "field": translate[rfields[j]] }))
        ccount = ccount+1

print(featureDesc[0:100])

sp500Prefix = cfg["features"]["sp500Prefix"]

# "/crypto/esoteric/tws/delayed-1623246971"
#import glob 
#lst = [f for f in glob.glob("/crypto/esoteric/tws/delayed-*")]
#lst.sort()
#print(lst)
#
#for f in lst:
#    try:
#        v = loadSP500File(f)
#    except:
#        pass
# loadSP500File("/crypto/esoteric/tws/delayed-1623246971")

class FeaturesSP500(Features):
    def getDescription(self)->List[Tuple[str,Dict[str,Any]]]:
        return featureDesc
    def getFeatureSize(self) -> int:
        return featureSize
    def getFeature(self, fromDT: datetime, toDT: datetime, timestep: timedelta) -> np.ndarray:
        import glob 
        lst = [f for f in glob.glob(sp500Prefix+"*")]
        lst.sort()
        print(lst)
        print(sp500Prefix)

        rv: List[np.ndarray] = []

        for f in lst:
            try:
                v = loadSP500File(f)
                rv.append(v)
            except:
                pass
        return np.vstack(rv)

def FeaturesSP500Builder(confg: Dict[str,Any])->Features:
    return FeaturesSP500()

registerFeatureBuilder("SP500", FeaturesSP500Builder)

