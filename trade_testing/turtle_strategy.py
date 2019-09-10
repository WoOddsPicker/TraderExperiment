import ta
import pandas as pd
import numpy as np
import warnings
from utils.utils import *


class TurtleStrategy:

    def __init__(self, prices, balance, atr_period = 48, entry_period=48, exit_period=24, max_entry=10, **kwargs):
        self.name = 'Turtle Trading'
        self.prices = prices
        self.balance = balance
        self.signals = pd.DataFrame({'ATR': ta.average_true_range(self.prices['High'], self.prices['Low'],self.prices['Close'], n=atr_period)})
        self.init_period = atr_period
        self.max_entry = max_entry

        self.entry_period = entry_period
        self.exit_period = exit_period
        self.entrySig= [0]
        self.exitSig = [0]
        self.stopSig = [0]
        self.unit = np.zeros(len(self.prices))

        self.entryFlag = False
        self.entryPrice = None
        self.entryCounter = 0

    def compute_unit(self, i):
        unit = 5 * self.balance / self.signals['ATR'][i]
        if unit > self.balance:
            warnings.warn('Unit valur bigger than balance', Warning)
        self.unit[i] = min(unit, self.balance)
        return unit

    def entry(self, i):
        if i < self.init_period:
            self.entrySig.append(0)
            return False
        else:
            if not self.entryFlag:
                if self.prices['High'][i]>max(self.prices['High'][i-self.entry_period:i]):
                    self.entrySig.append(1)
                    self.entryPrice = self.prices['High'][i]
                    self.entryCounter = self.entryCounter + 1
                    self.entryFlag = True
                    return True
                else:
                    self.entrySig.append(0)
                    return False
            else:
                if self.prices['High'][i] > self.entryPrice+self.signals['ATR'][i] and self.entryCounter<self.max_entry:
                    self.entrySig.append(1)
                    self.entryCounter = self.entryCounter+1
                    self.entryPrice = self.prices['High'][i]
                    return True
                else:
                    self.entrySig.append(0)
                    return False

    def exit(self, i):
        if self.entryFlag and self.prices['High'][i] - self.prices['High'][i-self.exit_period]<0:
            self.exitSig.append(-1)
            self.entryFlag = False
            self.entryPrice = None
            self.entryCounter =0
            return True
        else:
            self.exitSig.append(0)
            return False

    def stop(self, i):
        if self.entryFlag and self.prices['Low'][i-self.exit_period]-self.prices['Low'][i] > 2*self.signals['ATR'][i]:
            self.stopSig.append(-1)
            self.entryFlag = False
            self.entryPrice = None
            self.entryCounter = 0
            return True
        else:
            self.stopSig.append(0)
            return False


