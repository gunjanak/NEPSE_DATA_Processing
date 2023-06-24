#Enter a symbol and the code will tell you to buy it or not
from dataframe_nepse import stock_dataFrame
from obv import obv_column,buy_sell_obv


def process_OBV(df):
    df_obv = obv_column(df)
    df_buy_sell = buy_sell_obv(df_obv)
    

    return df_buy_sell

symbol = input("Enter a stock symbol: ")
weekly=False
weekly = bool(input("Enter True if you want decision based on weekly data: "))
try:
    df = stock_dataFrame(symbol,weekly=weekly)
except:
    pass
df_buy_sell = process_OBV(df)
print(df_buy_sell.tail())


decision = df_buy_sell['Buy_Sell'].tail(1).values[0]
print(decision)


if decision == 2:
    print(f"Buy the stocks of {symbol}")
elif decision == -2:
    print(f"Sell the stocks of {symbol}")
else:
    print(f"Hold")