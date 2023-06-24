#This will go through all the stocks listed in nepse
#Invest 10000 in all of them at begining of 2023-01-01
#Use MACD, OBV and JCS 
#compare their performance and suggest top 5 stocks to invest
import pandas as pd

from nepse_symbols import nepse_symbols
from dataframe_nepse import stock_dataFrame
from jcs import jcs_signals,jcs_strategy_I_profit,jcs_strategy_II_profit
from obv import obv_column, buy_sell_obv, profit_obv
from macd import macd, buy_sell_macd, profit_macd

def process_JCS(df):
    df_jcs = jcs_signals(df)
    #print(df_jcs.head())
    profit_jcs_I = jcs_strategy_I_profit(df_jcs)[0]
    profit_jcs_II = jcs_strategy_II_profit(df_jcs)[0]

    return [profit_jcs_I,profit_jcs_II]


def process_OBV(df):
    df_obv = obv_column(df)
    df_buy_sell = buy_sell_obv(df_obv)
    profit= profit_obv(df_buy_sell)[0]

    return profit

def process_MACD(df):
    df_macd = macd(df)
    df_buy_sell = buy_sell_macd(df_macd)
    profit  = profit_macd(df_buy_sell)[0]
    return profit

#get list of all the stocks
stock_list = nepse_symbols()

#stock_list = stock_list[:10]

stock_profit_JCS_I = {}
stock_profit_JCS_II = {}

stock_profit_OBV = {}
stock_profit_MACD = {}

Start_Date = input("Enter the Start Date in YYYY-MM-DD format:  ")

for stock in stock_list:
    print(stock)

    #read weekly dataframe from "2023-01-01"
    try:
        df = stock_dataFrame(stock,start_date=Start_Date,weekly=True)
        #print(df.head())
        jcs_process = process_JCS(df)
        stock_profit_JCS_I[stock] = jcs_process[0]
        stock_profit_JCS_II[stock] = jcs_process[1]

        stock_profit_OBV[stock] = process_OBV(df)
        stock_profit_MACD[stock] = process_MACD(df)



    except:
        pass

#df_JCS_I = pd.DataFrame(list(stock_profit_JCS_I.items()), columns=['Symbol', 'JCS_I_Profit'])
df_JCS_II = pd.DataFrame(list(stock_profit_JCS_II.items()), columns=['Symbol', 'JCS_II_Profit'])
df_OBV = pd.DataFrame(list(stock_profit_OBV.items()), columns=['Symbol', 'OBV_Profit'])
df_MACD = pd.DataFrame(list(stock_profit_MACD.items()), columns=['Symbol', 'MACD_Profit'])

df_JCS_I = pd.DataFrame.from_dict(stock_profit_JCS_I, orient='index', columns=['JCS_I_Profit'])
df_JCS_II = pd.DataFrame.from_dict(stock_profit_JCS_II, orient='index', columns=['JCS_II_Profit'])
df_OBV = pd.DataFrame.from_dict(stock_profit_OBV, orient='index', columns=['OBV_Profit'])
df_MACD = pd.DataFrame.from_dict(stock_profit_MACD, orient='index', columns=['MACD_Profit'])

print(df_JCS_I.head())
print(df_JCS_II.tail())
print(df_OBV.head())
print(df_MACD.head())



#combining into one
df = pd.DataFrame({"OBV_Profit":df_OBV['OBV_Profit'],"MACD_Profit":df_MACD['MACD_Profit'],
                   "JCS_I_Profit":df_JCS_I['JCS_I_Profit'],"JCS_II_Profit":df_JCS_II['JCS_II_Profit']})
#df['OBV_Profit'] = df_OBV['OBV_Profit']
#df['MACD_Profit'] = df_macd['MACD_Profit']
#df['Stochastic_Profit'] = df_stochastic['Stochastic_Profit']
#df['JCS_Profit'] = df_jcs['JCS_Profit']
print(df.head())

print(df.describe())
#finding best performing method i.e the method with highest average

# Calculate the mean for each column
mean_values = df.mean()
# Find the column with the highest mean
column_with_highest_mean = mean_values.idxmax()

# Display the column name with the highest mean
print("Method with the highest mean:", column_with_highest_mean)

#Method with highest maximum value
max_values = df.max()
method_with_highest_max = max_values.idxmax()
# Display the column name with the highest max
print("Method with the highest max:", method_with_highest_max)

#symbol for which this method got highest max
max_symbol = df.loc[df[method_with_highest_max].idxmax()]
print(f"Symbol with max profit \n {max_symbol}")

print("............................................................................")
#Best perfoming stock
#We will average performance of all the method  and print symbols with top 5 avgs
df2 = df
df["avg"] = df.mean(axis=1)
sorted_df = df.sort_values('avg')
print(sorted_df.tail(10))
print(sorted_df.tail(10).index)
first_list = sorted_df[-5:].index.tolist()

print("............................................................................")
#with nan removed
df2 = df2.dropna()
df2["avg"] = df2.mean(axis=1)
sorted_df = df2.sort_values('avg')
print(sorted_df.tail(10))
second_list = sorted_df[-5:].index.tolist()

high_profit_stocks = list(set(first_list).intersection(second_list))
print(f"The high_profit_stocks since {Start_Date} are as follows {high_profit_stocks}")
