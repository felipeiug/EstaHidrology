import pandas as pd
import numpy as np
from scipy.special import factorial

# Combinação de N por r
def C(N, r):
    r_0 = (isinstance(r, (np.ndarray, pd.Series)) and (r==0).all()) or r == 0
    if r_0:
        return 1
    
    N_arr_r = (isinstance(N, (np.ndarray, pd.Series)) and isinstance(r, (np.ndarray, pd.Series)) and (N==r).all())
    if N_arr_r:
        return 1
    
    N_r = not (isinstance(N, (np.ndarray, pd.Series)) or isinstance(r, (np.ndarray, pd.Series))) and N == r
    if N_r:
        return 1
    
    fac = factorial(N)/(factorial(r)*factorial(N-r))
    return fac

