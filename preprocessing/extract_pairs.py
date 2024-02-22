from fn.monad import Option

from fn import _

from fn.iters import map
from streams.Stream import Stream
import modin.pandas as pd
from streams.operations.operators import item
import numpy as np

from pair_request import Pair_Request

def json_to_df(json_data):
  df_json = pd.DataFrame.from_dict(json_data, orient="index").stack().to_frame()
  pairs_df = pd.DataFrame(df_json[0].values.tolist(), index=df_json.index)
  return (tuple(json_data.keys()), pairs_df)

def preprocess_pairs(symbol_pairs):
    pairs_df = (Stream
           .create(symbol_pairs)
           .map(lambda symbols_tuple: Pair_Request(symbols=symbols_tuple))
           .map(lambda pair_req: pair_req.execute())
           .map(lambda res: res.map(_.text).get_or("[]"))
           .map(lambda json_str: json.loads(json_str))
           .map(item['bars'])
	   .map(lambda pairs_bars_json: json_to_df(pairs_bars_json)).asList()))
    returns pairs_df


if __name__ == "__main__":

    from nasdaq_symbols import list_nasdaq_symbols

    nasdaq_pairs = list_nasdaq_symbols()
    pairs_df = preprocess_pairs(nasdaq_pairs)

            
