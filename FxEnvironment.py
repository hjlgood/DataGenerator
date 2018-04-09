from DataGenerator import DataGenerator
import numpy as np
import pandas as pd
import os, sys

# ohlc
path = sys.argv[0].split(os.path.basename(__file__))[0]
input_path = 'EURUSD1440.csv'
path = path+input_path
column_names = ['open','high','low','close']


class Environment(DataGenerator):
    def __init__(self, file_name,
                 lines,
                 position_size=1,
                 readtype='incremental',
                 account_size=10000):
        super().__init__(file_name, deliminator=',')

        # Currency name configuration
        self.numb_lines = lines
        self.read_type = readtype
        self.currency_name = input_path[0:6]   #EURUSD
        self.base_currency = self.currency_name[0:3] #EUR
        self.quote_currency = self.currency_name[3:6] #USD

        # State declarations
        self.current_state = None
        self.new_state = None
        
        # Action declarations
        self.action_space = ('long', 'short', 'flat')        
        self.action = None

        # Initial Account information
        self.pip_value = None
        self.position_size = position_size
        self.account_balance = account_size
        self.account_value = account_size
        self.set_pip_value()

    def set_pip_value(self):
        if self.quote_currency == 'USD':
            self.pip_value = 10

    def next_step(self, action, position=1):
        self.action = action
        self.set_states()
        print("Account Balance : {}, Account Value : {}".format(self.account_balance, self.account_value))
        
    def set_states(self):
        if self.current_state is None:
            self.current_state = self.get_data(self.numb_lines, readtype=self.read_type)
        elif self.new_state is None:
            self.new_state = self.get_data(self.numb_lines, readtype=self.read_type)            
        else:            
            self.current_state = self.new_state
            self.new_state = self.get_data(self.numb_lines, readtype=self.read_type)
            self.print_states()

    def print_states(self):
        if self.current_state is None:
            print("Current State is None!")
        else:
            print("Print current state: \n", self.current_state.tail(2))
        if self.new_state is None:
            print("New State is None!")
        else: 
            print("Print new state: \n", self.new_state.tail(2))
            
    def calculate_value_change(self, quote_currency = 'USD'):
        pip_change = (self.new_state.iloc[self.numb_lines-1,5] - self.current_state.iloc[self.numb_lines-1,5]) *10000
        dollar_change = pip_change *self.pip_value * self.position_size 
        return dollar_change


if __name__ == '__main__':
    env = Environment(path, lines=100, position_size=1)
    env.next_step(action= 'long')
    env.next_step(action= 'long')
    env.next_step(action= 'long')
    a = env.calculate_value_change()
    print(a)




