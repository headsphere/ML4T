"""MC1-P2: Optimize a portfolio."""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as spo
import datetime as dt
from util import get_data, plot_data


def calculate_sharpe_ratio(allocs, prices):
    sf = 252
    rfr = 0
    normed = prices / prices.iloc[0]
    pos_vals = normed * allocs
    port_val = np.sum(pos_vals, axis=1)
    daily_returns = (port_val / port_val.shift(1)) - 1
    daily_returns[0] = 0
    cr = (port_val[-1] / port_val[0]) - 1
    # exclude the first day
    adr = daily_returns[1:].mean()
    sddr = daily_returns[1:].std(ddof=1)
    sr = np.sqrt(sf) * (adr - rfr) / sddr
    return sr, adr, cr, sddr, port_val

# This is the function that will be tested by the autograder
# The student must update this code to properly implement the functionality
def optimize_portfolio(sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,1,1), \
    syms=['GOOG','AAPL','GLD','XOM'], gen_plot=False):

    # Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)  # automatically adds SPY
    prices = prices_all[syms]  # only portfolio symbols
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later

    def optimise_sharpe_ratio(x):
        y = calculate_sharpe_ratio(x, prices)
        return -1 * y[0]

    initial_allocs = [0.1, 0.2, 0.3, 0.4]
    cons = ({'type': 'eq', 'fun': lambda x:  1 - np.sum(x)})
    bnds = ((0, 1), (0, 1), (0, 1), (0, 1))
    min_sr = spo.minimize(optimise_sharpe_ratio, initial_allocs, method='SLSQP', options={'disp': True},
                          constraints=cons, bounds=bnds)

    sr, adr, cr, sddr, port_val = calculate_sharpe_ratio(min_sr.x, prices)

    # Compare daily portfolio value with SPY using a normalized plot
    if gen_plot:
        prices_SPY_normed = (prices_SPY/prices_SPY[0])
        df_temp = pd.concat([port_val, prices_SPY_normed], keys=['Portfolio', 'SPY'], axis=1)
        df_temp.plot()

        pass

    return initial_allocs, cr, adr, sddr, sr


def test_code():
    # This function WILL NOT be called by the auto grader
    # Do not assume that any variables defined here are available to your function/code
    # It is only here to help you set up and test your code

    # Define input parameters
    # Note that ALL of these values will be set to different values by
    # the autograder!

    start_date = dt.datetime(2010, 1, 1)
    end_date = dt.datetime(2010, 12, 31)
    symbols = ['GOOG', 'AAPL', 'GLD', 'XOM']

    # Assess the portfolio
    allocations, cr, adr, sddr, sr = optimize_portfolio(sd = start_date, ed = end_date,\
        syms = symbols, \
        gen_plot = True)

    # Print statistics
    print "Start Date:", start_date
    print "End Date:", end_date
    print "Symbols:", symbols
    print "Allocations:", allocations
    print "Sharpe Ratio:", sr
    print "Volatility (stdev of daily returns):", sddr
    print "Average Daily Return:", adr
    print "Cumulative Return:", cr

if __name__ == "__main__":
    # This code WILL NOT be called by the auto grader
    # Do not assume that it will be called
    test_code()
