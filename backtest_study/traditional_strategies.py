import pickle
import pandas as pd
from datetime import datetime
from trade_testing.backtesting import *
from trade_testing.turtle_strategy import TurtleStrategy
from trade_testing.hold_strategy import HoldStrategy
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('../data/coinbase_hourly.csv')
df = df.drop(['Symbol'], axis=1)
df['Date'] = df['Date'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %I-%p'))
df.index = df.index.values[::-1]
df.sort_index(ascending=True, inplace=True)

# Changing the start trade date
#df = df[13000:16000]
#df.index = df.index.values-13000

turtle_strategy = BackTest(df, 1000, TurtleStrategy, 0)
turtle_strategy.run_backtest()
turtle_strategy.plot_performance()

hold_strategy = BackTest(df, 1000, HoldStrategy, 0)
hold_strategy.run_backtest()
hold_strategy.plot_performance()



