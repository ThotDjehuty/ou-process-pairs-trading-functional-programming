import numpy as np
from streams.Stream import Stream
import modin.pandas as pd
from statsmodels.tsa.stattools import coint


def compute_spread_and_returns(df_by_pair):
  #Params : (symbol_1 and symbol_2)(Dataframe containing prices of a given pair indexed by time)
  #Returns : The following function (currying baby !) 
    #Params : symbol_1 and symbol_2 (should match with above dataframe)
    #Returns : (P_1) -> prices of the first asset
    #          (P_2) -> prices of the second asset
    #          (S) -> Spread
    # Synch both sampled times (may not match) to make spread correct
  symbols = df_by_pair[0]
  symb_1 = symbols[0]
  symb_2 = symbols[1]
  df_json = df_by_pair[1]
  P_1 = df_json.loc[symb_1][["c", "t"]].set_index("t")
  P_2 = df_json.loc[symb_2][["c", "t"]].set_index("t")

  index_without_jump = P_1.index.intersection(P_2.index)

  P_1 = P_1.loc[index_without_jump, :]
  P_2 = P_2.loc[index_without_jump, :]
  S = P_1 - P_2
  pair = "/".join((symb_1, symb_2))

  return {"pair": pair ,"P_1": P_1, "P_2": P_2, "S": S}


def cointegration_test(pair_spread):
  print(pair_spread["pair"])
  result = coint(pair_spread["P_1"], pair_spread["P_2"])
  pair_spread["cadf_pvalue"] = result[1]
  return pair_spread



if __name__ == "__main__":

    from preprocessing.nasdaq_symbols import list_nasdaq_symbols
    from preprocessing.extract_symbols import preprocess_pairs

    nasdaq_pairs = list_nasdaq_symbols()
    pairs_df = preprocess_pairs(nasdaq_pairs)

    cointegrated_pairs = (Stream
                  .create(pairs_df)
                  .filter(lambda pair: len(pair[0]) > 1)
                  .map(lambda df_pairs: compute_spread_and_returns(df_pairs))
                  .filter(lambda spread_by_pair: len(spread_by_pair["S"]) > 30)
                  .map(cointegration_test)
                  .filter(lambda spread: len(spread["S"]) > 15)
                  .filter(item['cadf_pvalue'] < 0.05)
                  .asList())




            
