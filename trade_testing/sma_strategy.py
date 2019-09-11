import ta
import pandas as pd
import numpy as np
import warnings
from utils.utils import *


class SmaStrategy:

    def __init__(self, prices, balance, atr_period=48, fast_period=12, slow_period = 26, signal_period=9, max_entry = 1,  **kwargs):
        self.name = 'SMA strategy'
        self.prices = prices
        self.balance = balance

        self.signals = pd.DataFrame()
        self.signals['ATR'] = ta.average_true_range(self.prices['High'], self.prices['Low'],self.prices['Close'], n=atr_period)
        self.signals['MACD'] = ta.macd(self.prices['Close'], n_fast=fast_period, n_slow=slow_period)
        self.signals['MACD_SIG'] = ta.macd_signal(self.prices['Close'], n_fast=fast_period, n_slow=slow_period, n_sign=signal_period)
        self.signals['MACD_HIST'] = ta.macd_diff(self.prices['Close'],  n_fast=fast_period, n_slow=slow_period, n_sign=signal_period)
        self.signals['MACD'].fillna(0)

        self.init_period = slow_period
        self.stop_period = 10

        self.max_entry = max_entry
        self.gamma_z = 0.1

        self.entrySig= [0]
        self.exitSig = [0]
        self.stopSig = [0]
        self.unit = np.zeros(len(self.prices))

        self.entryFlag = False
        self.entryPrice = None
        self.entryCounter = 0

    def compute_unit(self, i):
        unit = self.balance
        if unit > self.balance:
            warnings.warn('Unit value bigger than balance', Warning)
        self.unit[i] = min(unit, self.balance)
        unit = min(unit, self.balance)
        return unit

    def entry(self, i):
        if i < self.init_period:
            self.entrySig.append(0)
            return False
        else:
            if not self.entryFlag:
                if self.signals['MACD'][i]>0:
                    self.entrySig.append(1)
                    self.entryPrice = self.prices['Close'][i]
                    self.entryCounter = self.entryCounter + 1
                    self.entryFlag = True
                    return True
                else:
                    self.entrySig.append(0)
                    return False
            else:
                if self.signals['MACD'][i]>0 and self.signals['MACD'][i] > self.signals['MACD'][i-1] and self.entryCounter < self.max_entry:
                    self.entrySig.append(1)
                    self.entryCounter = self.entryCounter+1
                    self.entryPrice = self.prices['Close'][i]
                    return True
                else:
                    self.entrySig.append(0)
                    return False

    def exit(self, i):
        if self.signals['MACD'][i] < 0:
            self.exitSig.append(-1)
            self.entryFlag = False
            self.entryPrice = None
            self.entryCounter =0
            return True
        else:
            self.exitSig.append(0)
            return False

    def stop(self, i):
        if self.entryFlag and self.prices['Low'][i-self.stop_period]-self.prices['Low'][i] > 2*self.signals['ATR'][i]:
            self.stopSig.append(-1)
            self.entryFlag = False
            self.entryPrice = None
            self.entryCounter = 0
            return True
        else:
            self.stopSig.append(0)
            return False


