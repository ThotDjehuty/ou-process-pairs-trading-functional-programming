from fn.monad import Option
from fn.monad import optionable
from urllib import parse as urlparse

from fn import _

# url (example): url = "https://data.alpaca.markets/v2/stocks/bars?symbols=MSFT%2CAAPL&timeframe=1Min&start=2024-02-12T00%3A00%3A00Z&end=2024-02-13T00%3A00%3A00Z&limit=10000&adjustment=raw&feed=sip&currency=USD&sort=asc"
class Pair_Request:
  def __init__(self,
               symbols,
               header=query_headers,
               start_date="2024-02-12T00%3A00%3A00Z",
               end_date="2024-02-13T00%3A00%3A00Z"):
        self.header = header
        self.start_date =start_date
        self.end_date = end_date
        self.symbols = symbols
        self.timeframe = "1Min"
        self.base_url = "https://data.alpaca.markets/v2/stocks/bars?symbols="
        self.query_params = self.set_query_params()
        self.url = self.base_url + self.set_query_params()


  def concat_symbols(self) -> str:
    return self.symbols[0] + "%2C" + self.symbols[1]


  def set_query_params(self) -> str:
    query_params = {"timeframe": self.timeframe,
          "start": self.start_date, "end": self.end_date,
          "limit": "10000&adjustment=raw&feed=sip&currency=USD&sort=asc"}
    return self.concat_symbols() + "&" + "&".join('='.join(param) for param in query_params.items())

  @optionable
  def execute(self):
    return requests.get(self.base_url + self.set_query_params(), headers=query_headers)
