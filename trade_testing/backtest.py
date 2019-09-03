from utils.utils import *

class BackTest:
    def __init__(self, BTC_prices, initial_balance, strategy_signal, commission=0):
        self.BTC_prices = BTC_prices
        self.net_worths = [initial_balance]
        self.balance = initial_balance
        self.amount_held = 0
        self.strategy_signal = strategy_signal
        self.commission = commission

    def run_backtest(self):
        signal = self.strategy_signal(self.BTC_prices)
        for i in range(1, len(self.BTC_prices)):
            if self.amount_held > 0:
                self.net_worths.append(self.balance + self.amount_held * self.BTC_prices[i])
            else:
                self.net_worths.append(self.balance)

            if signal(i) == SIGNALS.SELL and self.amount_held > 0:
                self.balance = self.amount_held * (self.BTC_prices[i] * (1 - self.commission))
                self.amount_held = 0
            elif signal(i) == SIGNALS.BUY and self.amount_held == 0:
                self.amount_held = self.balance / (self.BTC_prices[i] * (1 + self.commission))
                self.balance = 0
        return self.net_worths
