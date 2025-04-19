#!/usr/bin/env python
# coding: utf-8

# In[25]:


#use pandas, datetime, and time.

import pandas as pd
import datetime
import time 
import numpy as np
from yahooquery import Ticker 
pd.set_option('display.max_rows',None)
symbol = 'AAPL'
stock = Ticker(symbol)
print(stock.cash_flow())


# In[49]:


###Get  Historical FCP (cre8 simple forcast of future FCF based on previous FCP grwoth raio.

df_cash = pd.DataFrame(stock.cash_flow())
print(df_cash.columns)
df_cash['asOfDate'] = pd.to_datetime(df_cash['asOfDate'])
df_cash.set_index('asOfDate', inplace = True)
df_cash = df_cash.sort_index()
df_cash = df_cash[['FreeCashFlow']].dropna()


# In[35]:


##### get historic net debt

df_balance= pd.DataFrame(stock.balance_sheet())
df_balance['asOfDate'] = pd.to_datetime(df_balance['asOfDate'])
df_balance.set_index('asOfDate',inplace=True)

df_balance = df_balance.sort_index()
df_balance = df_balance[['NetDebt']].dropna()
print(df_balance)



# In[45]:


####net debt value
net_debt = df_balance['netDebt'].iloc[-1]



# In[47]:


###create a convert LIST FUNCTION FOR FUTURE WRANGLING

def column_to_list(df,column_name):
    data_list = df[column_name].tolist()
    data_list = [x for x in data_list if pd.notnull(x)]
    return data_list


####
historic_fcf = column_to_list(df_cash, 'freeCashFlow')



# In[41]:


####CALC AVG GROWTH RATE OF FCF FOR SIMPLE FORECASTING



fcf_growth_rates = [(historic_fcf[i] - historic_fcf[i-1]) / historic_fcf[i-1] for i in range[1, len(historic_fcf))]
fcf_avg_growth_rate = np.mean(fcf_growth_rates)








# In[43]:


s#####Future projections###

#forecast future FCFS
future_years = 5
future_fcfs = [historic_fcf[-1]*(1+fcf_avg_growth_rate)**(i+1) for i in range(future_years)]

#discount future FCF
discount_rate = 0.10
discount_fcfs = [fcf / (1 + discount_rate) ** (i+1) for i, fcf in enumerate(future_fcfs)]

# clc TERMINAL VALUE
termina_value = future_value / (1 + discount_rate) **future_years

# calc Total Enterprise Value 
enterprise_value = sum(disocunted_fcfs + discounted_terminal_value)

#subtract net debt to get equity value
equity_value = enterprise_value - net_debt

print("Enterprise Value: ${enterprise_value:, .2f}")
print(f"Equity Value: ${equity_value:, 2f}")
















