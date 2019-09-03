import pickle
import pandas as pd
from datetime import datetime
from trade_testing.backtest import *
from trade_testing.strategies import sma_crossover, buy_and_hodl, rsi_divergence
import matplotlib.pyplot as plt
df = pd.read_csv('../data/coinbase_hourly.csv')
df = df.drop(['Symbol'], axis=1)
df['Date'] = df['Date'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %I-%p'))
df.index = df.index.values[::-1]
df.sort_index(ascending=True, inplace=True)

# Changing the start trade date
#df = df[13000:16000]
#df.index = df.index.values-13000

macd_backtest = BackTest(df['Close'], 1000, sma_crossover, 0)
rsi_backtest = BackTest(df['Close'], 1000, rsi_divergence, 0)
buy_and_hodl_backtest = BackTest(df['Close'], 1000, buy_and_hodl, 0)

net_worth_macd = macd_backtest.run_backtest()
net_worth_rsi = rsi_backtest.run_backtest()
net_worth_buyhold = buy_and_hodl_backtest.run_backtest()

plt.subplot(211)
plt.title('Evolução do preço do Bitcoin')
plt.xlabel('Data')
plt.ylabel('Preço (USD)')
plt.grid()
plt.plot(df['Date'], df['Close'])
plt.subplot(212)

plt.title('Evolução dos ganhos usando MACD/RSI startegy')
plt.xlabel('Data')
plt.ylabel('Saldo (USD)')
plt.plot(df['Date'], net_worth_macd, label='MACD')
plt.plot(df['Date'], net_worth_rsi, label='RSI')
plt.plot(df['Date'], net_worth_buyhold, label='BUYHOLD')
plt.legend()
plt.grid()
plt.show()