import pandas as pd
import math

def obv_column(company_df):
  length = len(company_df)
  #print(length)
  OBV = 0
  obv_daily = []
  for i in range(length-1):
    if(company_df['Close'][i+1] > company_df['Close'][i]):
      OBV = OBV + company_df['Volume'][i+1]
      obv_daily.append(OBV)
    elif (company_df['Close'][i+1] < company_df['Close'][i]):
      OBV = OBV - company_df['Volume'][i+1]
      obv_daily.append(OBV)
    else:
      OBV = OBV
      obv_daily.append(OBV)
  company_df2 = company_df
  # Drop first row
  company_df2.drop(index=company_df2.index[0],
        axis=0,
        inplace=True)

  company_df2['OBV'] = obv_daily
  #print(len(company_df2))
  return company_df2

def buy_sell_obv(company_df):
  company_df2 = company_df
  length = len(company_df2)
  #print(length)
  buy_sell = []
  signal = 0
  for i in range(length-1):
    if (company_df2['OBV'][i+1]>company_df2['OBV'][i]):
      signal = 2
      buy_sell.append(signal)
    elif (company_df2['OBV'][i+1] < company_df2['OBV'][i]):
      signal = -2
      buy_sell.append(signal)
    else:
      signal = 0
      buy_sell.append(signal)

  company_df3 = company_df2
  # Drop first row
  company_df3.drop(index=company_df3.index[0], axis=0, inplace=True)
  #print(len(buy_sell))
  company_df3['Buy_Sell'] = buy_sell
  #print(len(company_df3))
  return company_df3


def profit_obv(company_df,seed_money=10000):
  company_df3 = company_df
  length = len(company_df3)
  money = seed_money
  shares = 0
  last_buy_price = 0
  flag = 0
  for i in range(length):
    if((company_df3['Buy_Sell'][i] == 2)&(flag == 0)):
      #print('Buying share at: ')
      #print(company_df3['Close'][i])
      #print('Date: ')
      #print(company_df3.index[i])
      shares = math.floor(money/company_df3['Close'][i])
      #print(shares)
      money = money - shares*company_df3['Close'][i]
      last_buy_price = company_df3['Close'][i]
      #print(money)
      #print('\n')
      flag = 1

    elif((company_df3['Buy_Sell'][i] == -2) & (company_df3['Close'][i] > last_buy_price) & (flag == 1)):
      #print('Selling share at: ')
      #print(company_df3['Close'][i])
      new_money = shares*company_df3['Close'][i]
      shares = 0
      #print(new_money)
      money = money + new_money
      #print(money)
      #print('\n\n')
      flag = 0

  final_money = shares*company_df3['Close'][-1] + money
  return [final_money,shares,money]





