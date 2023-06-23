from nepse_symbols import nepse_symbols

from dataframe_nepse import stock_dataFrame
from obv import obv_column,buy_sell_obv,profit_obv

from jcs import jcs_signals, jcs_strategy_I_profit, jcs_strategy_II_profit

from macd import macd, buy_sell_macd,profit_macd

all_symbols = nepse_symbols()
print(all_symbols)

df = stock_dataFrame("NTC")
print(df.tail())

df = stock_dataFrame("NTC","2023-01-01")
print(df.head())

df = stock_dataFrame("NTC","2023-01-01",weekly=True)
print(df.head())

df_obv = obv_column(df)
print(df_obv.head())

df_buy_sell = buy_sell_obv(df_obv)
print(df_buy_sell.tail())

print(profit_obv(df_buy_sell)[0])

df_jcs = jcs_signals(df)
print(df_jcs.tail())
print(jcs_strategy_I_profit(df_jcs))
print(jcs_strategy_II_profit(df_jcs))


df_macd = macd(df)
print(df_macd.head())
df_buy_sell = buy_sell_macd(df_macd)
print(profit_macd(df_buy_sell))