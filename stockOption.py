import math

from stockVolatility import stock_vol

class stockoption():

    def __init__(self, S0, K, r, T, N, prm):
        # S0 = initial stock price
        # K = strike price
        # r = risk free rate of interest per year
        # T = length of the option, in years
        # N = number of binomial iterations 
        # prm = dictionary with additional parameters 

        self.S0 = S0
        self.K = K
        self.r = r
        self.N = N
        self.prm = prm
        

        # prm parameters 
        # start = start date, "yyyy-mm-dd"
        # end = end date, "yyyy-mm-dd"
        # tk = ticker label
        # div = dividend paid 
        # is_calc = is volatility calculated using stock price history, boolean
        # use_garch = use Garch model, boolean
        # sigma = volatility of stock
        # is_call = is it a call option, boolean
        # eu_option = European or American option, boolean 

        # get() returns a value for the given key
        # if key is NOT available, then returns default value None
        self.tk = prm.get('tk', None)
        self.start = prm.get('start', None)
        self.end = prm.get('end', None)
        self.div = prm.get('div', 0) # if no dividend, then return 0
        self.is_calc = prm.get('is_calc', False)
        self.use_garch = prm.get('use_garch', False)

        self.vol = stock_vol(self.tk, self.start, self.end)

        if self.is_calc:
            if self.use_garch:
                self.sigma = self.vol.garch_sigma()
            else:
                self.sigma = self.vol.mean_sigma()
        else:
            self.sigma = prm.get('sigma', 0)

        self.is_call = prm.get('is_call', True)
        self.eu_option = prm.get('eu_option', True)

        # DERIVED VALUES
        # dt = time per step, in years
        self.dt = T / float(N)
        # df = discount factor 
        self.df = math.exp(-(r-self.div)*self.dt)




        