from utils.utils import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib


class BackTest:
    def __init__(self, dataframe, initial_balance, strategy, commission=0, op_eval = ["High","High", "High", "Close"],  **kwargs):
        self.dataframe = dataframe
        self.net_worths = np.array([initial_balance])
        self.balance_ev = np.array([initial_balance])
        self.held_ev = np.array([0])
        self.balance = initial_balance
        self.amount_held = 0
        self.strategy = strategy(dataframe, initial_balance, **kwargs)
        self.commission = commission
        self.op_eval = op_eval # Entry, Exit, Stop, Compute

    def run_backtest(self):
        for i in range(1, len(self.dataframe)):
            unit = self.strategy.compute_unit(i)
            self.balance_ev=np.append(self.balance_ev, self.balance)
            self.held_ev=np.append(self.held_ev, self.amount_held * self.dataframe[self.op_eval[3]][i])
            if self.amount_held > 0:
                self.net_worths = np.append(self.net_worths, self.balance + self.amount_held * self.dataframe[self.op_eval[3]][i])
            else:
                self.net_worths = np.append(self.net_worths, self.balance)

            entry_flag = self.strategy.entry(i)
            exit_flag = self.strategy.exit(i)
            stop_flag = self.strategy.stop(i)
            if entry_flag:
                entry_unit = self.strategy.unit[i]
                self.amount_held = self.amount_held + entry_unit / (self.dataframe[self.op_eval[0]][i] * (1 + self.commission))
                self.balance = self.balance-entry_unit
            if exit_flag and not entry_flag:
                units_sold = self.amount_held * (self.dataframe[self.op_eval[1]][i] * (1 - self.commission))
                self.balance = self.balance+units_sold
                self.amount_held = 0
            if stop_flag and not entry_flag and not exit_flag:
                units_sold = self.amount_held * (self.dataframe[self.op_eval[2]][i] * (1 - self.commission))
                self.balance = self.balance + units_sold
                self.amount_held = 0
            self.strategy.balance = self.balance
        return self.net_worths

    def plot_performance(self):
        fig, ax = plt.subplots(2, sharex=True)
        ax[0].set_title('Evolução do preço do Bitcoin')
        ax[0].set(xlabel='Data')
        ax[0].set(ylabel='Preço (USD)')
        ax[0].grid()
        ax[0].plot(self.dataframe['Date'], self.dataframe['Close'])

        ax[1].set_title('Evolução dos ganhos da estratégia:' + self.strategy.name)
        ax[1].set(xlabel='Data')
        ax[1].set(ylabel='Saldo (USD)')
        ax[1].plot(self.dataframe['Date'], self.net_worths)
        ax[1].plot(self.dataframe['Date'], self.balance_ev, label='balance')
        ax[1].plot(self.dataframe['Date'], self.held_ev, label='held')
        ax[1].legend()
        ax[1].grid()
        plt.show()

    def plot_buy_exit(self):
        fig, ax = plt.subplots(2, sharex=True)
        ax[0].set_title('Evolução do preço do Bitcoin')
        ax[0].set(xlabel='Data')
        ax[0].set(ylabel='Preço (USD)')
        ax[0].grid()
        ax[0].plot(self.dataframe['Date'], self.dataframe['Close'])

        ax[1].set_title('Evolução dos ganhos da estratégia:' + self.strategy.name)
        ax[1].set(xlabel='Data')
        ax[1].set(ylabel='Saldo (USD)')
        ax[1].plot(self.dataframe['Date'], self.strategy.entrySig, label='Entry')
        ax[1].plot(self.dataframe['Date'], self.strategy.exitSig, label='Exit')
        ax[1].legend()
        ax[1].grid()
        plt.show()


