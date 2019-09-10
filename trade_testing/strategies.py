import ta
from utils.utils import *


def buy_and_hodl(prices):
    def signal_fn(i):
        return SIGNALS.BUY
    return signal_fn

def rsi_divergence(prices, period=3):
    rsi = ta.rsi(prices)

    def signal_fn(i):
        rsiSum = sum(rsi[i - period:i + 1].diff().cumsum().fillna(0))
        priceSum = sum(prices[i - period:i + 1].diff().cumsum().fillna(0))

        if i >= period:
            if rsiSum < 0 and priceSum >= 0:
                return SIGNALS.BUY
            elif rsiSum > 0 and priceSum <= 0:
                return SIGNALS.SELL

        return SIGNALS.HOLD

    return signal_fn


def sma_crossover(prices):
    macd = ta.macd(prices)

    def signal_fn(i):
        if macd[i] > 0 and macd[i - 1] <= 0:
            return SIGNALS.BUY
        elif macd[i] < 0 and macd[i - 1] >= 0:
            return SIGNALS.SELL

        return SIGNALS.HOLD

    return signal_fn

def buy_and_hodl(prices=None):
    def signal_fn(i):
        return SIGNALS.BUY
    return signal_fnd