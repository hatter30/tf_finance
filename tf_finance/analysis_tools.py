import numpy as np
import scipy.optimize as sco
from functools import partial

def pct_change(df):
    pct_change = (1 - df / df.shift(1)).shift(-1)
    pct_change = pct_change.dropna()
    return pct_change
    
def returns(df):
    return np.log(df / df.shift(-1))
    
def sampling_rets_vols(rets, num_sample=2500, num_year=252):
    noa = rets.shape[1]
    prets = []
    pvols = []
    for p in range (num_sample):
        weights = np.random.random(noa)
        weights /= np.sum(weights)
        prets.append(np.sum(rets.mean() * weights) * num_year)
        pvols.append(np.sqrt(np.dot(weights.T, 
                            np.dot(rets.cov() * num_year, weights))))
    prets = np.array(prets)
    pvols = np.array(pvols)
    return prets, pvols
    
def statistics(weights, ret_df):
    weights = np.array(weights)
    pret = np.sum(ret_df.mean() * weights) * 252
    pvol = np.sqrt(np.dot(weights.T, np.dot(ret_df.cov() * 252, weights)))
    return np.array([pret, pvol, pret / pvol])

  
    
def max_sharpe_point(rets):
    noa = rets.shape[1]

    statistics_rets = partial(statistics, ret_df=rets)  

    def min_func_sharpe(weights):
        return -statistics_rets(weights)[2]

    cons = ({'type': 'eq', 'fun': lambda x:  np.sum(x) - 1})

    bnds = tuple((0, 1) for x in range(noa))

    opts = sco.minimize(min_func_sharpe, noa * [1. / noa,], method='SLSQP',
                           bounds=bnds, constraints=cons)

    return opts['x']
    
    
def min_variance_point(rets):
    noa = rets.shape[1]
    
    statistics_rets = partial(statistics, ret_df=rets)  
    
    def min_func_variance(weights):
        return statistics_rets(weights)[1] ** 2
    
    cons = ({'type': 'eq', 'fun': lambda x:  np.sum(x) - 1})
    
    bnds = tuple((0, 1) for x in range(noa))
    
    optv = sco.minimize(min_func_variance, noa * [1. / noa,], method='SLSQP',
                           bounds=bnds, constraints=cons)
    
    return optv['x']