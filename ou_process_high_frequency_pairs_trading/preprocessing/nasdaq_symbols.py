from fn.monad import Option
from fn.monad import optionable
from urllib import parse as urlparse

from fn import _

from fn.iters import map
from itertools import chain, combinations
from streams.Stream import Stream
import modin.pandas as pd
from streams.operations.operators import item

symbs_custom = ["MSFT", "AAPL", "AMZN", "NVDA", "META", "AVGO", "TSLA", "GOOGL", "AMD", "NFLX", "AEP", "MCHP", "NXPI"]
pairs_custom = list(combinations(symbs_custom, 2))

def list_nasdaq_symbols():
  url = 'https://en.m.wikipedia.org/wiki/Nasdaq-100'
  wiki_df = pd.read_html(url,
                         attrs={'id': "constituents"},
                         index_col='Ticker')[0]
  nasdaq_symbols = wiki_df.index.to_list()
  return list(combinations(nasdaq_symbols, 2))

if __name__ == "__main__":
    from data_generation import generate_synthetic_data
    S1, S2_adjusted = generate_synthetic_data()
    spread_data = S2_adjusted - S1
    mu_calibrated, theta_calibrated, sigma_calibrated = calibrate_OU(spread_data)
    print(f"Calibrated Parameters - mu: {mu_calibrated}, theta: {theta_calibrated}, sigma: {sigma_calibrated}")
