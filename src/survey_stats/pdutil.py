import pandas as pd
import numpy as np

#extend Series with fill_none method
# to take care of json/mysql conversion
def fill_none(self):
    return self.where(pd.notnull(self),None)

def guard_nan(val):
    return None if np.isnan(val) else val

