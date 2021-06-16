

import http.client
from Config import cfg
from Fetcher import *
from LimiterMonthly import *
import json

class FetcherYahoo(Fetcher):
    def __init__(self, stock:str, queryType:str, region:str):
        self.stock = stock
        self.queryType = queryType
        self.region = region
    def setLimiter(self, l: Limiter):
        self.limiter = l
    def tryFetch(self) -> bool:
        ok = self.limiter.canDo({}, datetime.now())
        return ok
    def fetch(self):
        self.limiter.recordDo({}, datetime.now())
        print(self.queryType)
        try:
            if self.queryType == "BalanceSheet":
                r = self.stockBalanceSheet()
                r["fetcherTag"] = self.tag()
                return r
            if self.queryType == "NewsList":
                r = self.newsList()
                r["fetcherTag"] = self.tag()
                return r                
            if self.queryType == "Recommendations":
                r = self.recommendations()
                r["fetcherTag"] = self.tag()
                return r                
        except Exception as e:
            print(e)
        return {}
    def tag(self) -> str:
        return "Yahoo-" + self.stock + "-" + self.queryType + "-" + self.region
    def makeHeader(self):
        return {
            'content-type': "text/plain",
            'x-rapidapi-key': cfg["rapidapi"]["x-rapidapi-key"],
            'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com"
        }
    def stockBalanceSheet(self): # not working
        print("stockBalanceSheet", self.stock, self.queryType, self.region)
        headers = self.makeHeader()
        conn = http.client.HTTPSConnection("apidojo-yahoo-finance-v1.p.rapidapi.com")
        conn.request("GET", "/stock/v2/get-balance-sheet?symbol="+self.stock+"&region="+self.region, headers=headers)
        res = conn.getresponse()
        data = res.read()
        print("raw response", data)
        x = data.decode("utf-8")
        return json.loads(x)
    def newsList(self):
        print("newsList", self.stock, self.queryType, self.region)
        headers = self.makeHeader()
        conn = http.client.HTTPSConnection("apidojo-yahoo-finance-v1.p.rapidapi.com")
        payload = ""
        conn.request("POST", "/news/v2/list?region="+self.region+"&snippetCount=28", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print("raw response", data)
        x = data.decode("utf-8")
        return json.loads(x)    
    def recommendations(self): # not working
        print("recommendations", self.stock, self.queryType, self.region)
        headers = self.makeHeader()
        conn = http.client.HTTPSConnection("apidojo-yahoo-finance-v1.p.rapidapi.com")
        conn.request("GET", "/stock/v2/get-recommendations?symbol=" + self.stock, headers=headers)
        res = conn.getresponse()
        data = res.read()
        print("raw response", data)
        x = data.decode("utf-8")
        return json.loads(x)

def FetcherYahooBuilder(cfg: Dict[str,Any]) -> Fetcher:
    print("fetcher config", cfg)
    return FetcherYahoo(cfg["stock"], cfg["queryType"], cfg["region"])
registerFetcherBuilder("Yahoo", FetcherYahooBuilder)
