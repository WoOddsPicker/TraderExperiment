import ta
import pandas as pd
import numpy as np
import warnings
from utils.utils import *


class HoldStrategy:

    def __init__(self, prices, balance, **kwargs):
        self.name = 'Hold 4ever'
        self.prices = prices
        self.balance = balance
        self.entrySig= [0]
        self.exitSig = [0]
        self.stopSig = [0]
        self.unit = np.zeros(len(self.prices))

        self.entryFlag = True
        self.entryPrice = None
        self.entryCounter = 0

    def compute_unit(self, i):
        unit = self.balance
        self.unit[i] = unit
        if unit > self.balance:
            warnings.warn('Unit valur bigger than balance', Warning)
        return unit

    def entry(self, i):
        if not self.entryFlag:
            self.entrySig.append(0)
            return False
        else:
            self.entrySig.append(1)
            self.entryPrice = self.prices['Close'][i]
            self.entryCounter = self.entryCounter + 1
            self.entryFlag = False
            return True

    def exit(self, i):
        self.exitSig.append(0)
        return False

    def stop(self, i):
        self.stopSig.append(0)
        return False


