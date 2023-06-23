import math


def macd(company_df):
  company_df2 = company_df
  company_df['EMA_12'] = company_df['Close'].ewm(span=12, adjust=False).mean()
  company_df['EMA_9'] = company_df['Close'].ewm(span=9, adjust=False).mean()
  company_df['MACD'] = company_df['EMA_12'] - company_df['EMA_9']
  company_df['MACD_signal'] = company_df['MACD'].ewm(span=9, adjust=False).mean()
  company_df['Difference'] = company_df['MACD'] - company_df['MACD_signal']

  company_df2['MACD_Diff'] = company_df['Difference']
  return company_df2



def buy_sell_macd(company_df):
  company_df4 = company_df
  length = len(company_df4)
  buy_sell = []
  for i in range(1,(length),1):
    if (company_df4['MACD_Diff'][i]<0) & (company_df4['MACD_Diff'][i-1]>0):
      buy_sell.append(-2)
    elif (company_df4['MACD_Diff'][i]>0) & (company_df4['MACD_Diff'][i-1]<0):
      buy_sell.append(2)
    else:
      buy_sell.append(0)

  # Drop first row
  company_df4.drop(index=company_df4.index[0],
        axis=0,
        inplace=True)
  company_df4['Buy_Sell'] = buy_sell

  return company_df4

def profit_macd(company_df,seed_money=10000):
  money = seed_money
  company_df3 = company_df
  length = len(company_df3)
  shares = 0
  last_buy_price = 0
  flag = 0
  for i in range(length):
    if ((company_df3['Buy_Sell'][i] == 2)&(flag == 0)):
      shares = math.floor(money/company_df3['Close'][i])
     
      money = money - shares*company_df3['Close'][i]
      last_buy_price = company_df3['Close'][i]
      flag = 1

    elif ((company_df3['Buy_Sell'][i] == -2) & (company_df3['Close'][i] > last_buy_price) & (flag == 1)):
     
      new_money = shares*company_df3['Close'][i]
      shares = 0
  
      money = money + new_money
 
      flag = 0

  return [shares*company_df3['Close'][-1] + money,shares,money]