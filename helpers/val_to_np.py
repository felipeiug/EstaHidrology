import pandas as pd
import numpy as np

def val_to_np(val:float|int|pd.Series|np.ndarray|list|set|tuple)->np.ndarray:
    if isinstance(val, pd.Series):
        val = val.values
    elif isinstance(val, (list, set, tuple, float, int)):
        val = np.array(val)
    
    return val

