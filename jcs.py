#japanese candle stick


import pandas as pd
import requests
from io import StringIO
from datetime import datetime, timedelta
import math


def jcs_signals(df):
    for i in range(2,df.shape[0]):
      current = df.iloc[i,:]
      prev = df.iloc[i-1,:]
      prev_2 = df.iloc[i-2,:]

      realbody = abs(current['Open'] - current['Close'])
      candle_range = current['High'] - current['Low']

      idx = df.index[i]

      # Bullish swing
      df.loc[idx,'Bullish swing'] = current['Low'] > prev['Low'] and prev['Low'] < prev_2['Low']

      # Bearish swing
      df.loc[idx,'Bearish swing'] = current['High'] < prev['High'] and prev['High'] > prev_2['High']

      # Bullish pinbar
      df.loc[idx,'Bullish pinbar'] = realbody <= candle_range/3 and  min(current['Open'], current['Close']) > (current['High'] + current['Low'])/2 and current['Low'] < prev['Low']

      # Bearish pinbar
      df.loc[idx,'Bearish pinbar'] = realbody <= candle_range/3 and max(current['Open'] , current['Close']) < (current['High'] + current['Low'])/2 and current['High'] > prev['High']

      # Inside bar
      df.loc[idx,'Inside bar'] = current['High'] < prev['High'] and current['Low'] > prev['Low']

      # Outside bar
      df.loc[idx,'Outside bar'] = current['High'] > prev['High'] and current['Low'] < prev['Low']

      # Bullish engulfing
      df.loc[idx,'Bullish engulfing'] = current['High'] > prev['High'] and current['Low'] < prev['Low'] and realbody >= 0.8 * candle_range and current['Close'] > current['Open']

      # Bearish engulfing
      df.loc[idx,'Bearish engulfing'] = current['High'] > prev['High'] and current['Low'] < prev['Low'] and realbody >= 0.8 * candle_range and current['Close'] < current['Open']




    return df


def jcs_strategy_I_profit(company_df,seed_money=10000):
  length = len(company_df)

  money = seed_money
  shares = 0
  last_buy_price = 0
  flag = 0
  net_worth = []
  net_worth_value = money

  for i in range(length):
    if((company_df['Bullish swing'][i]==True)&(flag == 0)):
      #print('Buying share at: ')
      #print(company_df['Close'][i])
      #print('Date: ')
      #print(company_df['Date'][i])
      shares = math.floor(money/company_df['Close'][i])
      #print(shares)
      money = money - shares*company_df['Close'][i]
      last_buy_price = company_df['Close'][i]
      #print(money)
      net_worth_value = shares*company_df['Close'][i] + money
      net_worth.append(net_worth_value)
      #print('\n')
      flag = 1

    elif((company_df['Bearish swing'][i]==True)&(flag == 1)):
      #print('Selling share at: ')
      #print(company_df['Close'][i])
      new_money = shares*company_df['Close'][i]
      shares = 0
      #print(new_money)
      money = money + new_money
      #print(money)
      net_worth_value = money
      net_worth.append(net_worth_value)
      #print('\n\n')
      flag = 0
    else:
      if(flag == 1):
        net_worth_value = shares*company_df['Close'][i] + money
        net_worth.append(net_worth_value)
      else:
        net_worth.append(net_worth_value)

  return [shares*company_df['Close'][length-1] + money,shares,money]




def jcs_strategy_II_profit(company_df,seed_money=10000):
  
  length = len(company_df)

  money = seed_money
  shares = 0
  last_buy_price = 0
  flag = 0
  net_worth = []
  net_worth_value = money

  for i in range(length):
    if((company_df['Bullish engulfing'][i]==True)&(flag == 0)):
      #print('Buying share at: ')
      #print(company_df['Close'][i])
      #print('Date: ')
      #print(company_df['Date'][i])
      shares = math.floor(money/company_df['Close'][i])
      #print(shares)
      money = money - shares*company_df['Close'][i]
      last_buy_price = company_df['Close'][i]
      #print(money)
      net_worth_value = shares*company_df['Close'][i] + money
      net_worth.append(net_worth_value)
      #print('\n')
      flag = 1

    elif((company_df['Bearish engulfing'][i]==True)&(flag == 1)):
      #print('Selling share at: ')
      #print(company_df['Close'][i])
      new_money = shares*company_df['Close'][i]
      shares = 0
      #print(new_money)
      money = money + new_money
      #print(money)
      net_worth_value = money
      net_worth.append(net_worth_value)
      #print('\n\n')
      flag = 0
    else:
      if(flag == 1):
        net_worth_value = shares*company_df['Close'][i] + money
        net_worth.append(net_worth_value)
      else:
        net_worth.append(net_worth_value)

  #print(shares*company_df['Close'][length-1] + money)

  return [shares*company_df['Close'][length-1] + money,shares,money]
