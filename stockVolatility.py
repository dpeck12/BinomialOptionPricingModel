import numpy as np
import pandas as pd 

import pandas_datareader.data as pdr 
import yfinance as yf # slight difference

import arch

import matplotlib.pyplot as plt 

from statsmodels.graphics.tsaplots import plot_acf 

yf.pdr_override()

class stock_vol:

    def __init__(self, ticker, start, end):

        self.ticker = ticker;
        self.start = start;
        self.end = end;

        all_data = pdr.get_data_yahoo(self.ticker, start=self.start, end=self.end)
        self.stock_data = pd.DataFrame(all_data['Adj Close'], columns=["Adj Close"])

        # np.log is natural logarithm
        # dataframe.shift() function Shift index by desired number of periods
        # with an optional time freq. Takes scalar parameter period 
        self.stock_data["log"] = np.log(self.stock_data) - np.log(self.stock_data.shift(1))


    def mean_sigma(self):
        # dropna() remove missing values 
        # ewm() provid exponential weighted functions (EW)
        # mean(), var(), std(), corr(), cov()
        # specify decay in terms of span, alpha=2/(span+1), for some span>=1
        # 253 trading days in a year
        st = self.stock_data["log"].dropna().ewm(span=252).std()
        # iloc[-1], last row of data frame
        sigma = st.iloc[-1]
        return sigma 

    def garch_sigma(self):
        # using 'Zero' mean model 
        # using 'GARCH' volatility model
        # p = Lag order of symmetric innovation
        # q = Lag order of lagged volatility or equivalent 
        model = arch.arch_model(self.stock_data["log"].dropna(), mean='Zero', vol='GARCH', p=1, q=1)
        model_fit = model.fit() 
        # positive integer value indicating the maximum horizon to produce forecasts
        forecast = model_fit.forecast(horizon=1)
        var = forecast.variance.iloc[-1]
        sigma = float(np.sqrt(var))
        return sigma 

if __name__ == "__main__":
    vol = stock_vol("AAPL", start="2016-01-01", end="2016-03-01")
    test = vol.stock_data["log"].dropna()
    print(test)
    fig = plot_acf(test)
    plt.show()
