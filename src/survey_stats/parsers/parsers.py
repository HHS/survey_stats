import pandas as pd

def parse(self, filename, col_names, col_specs):
    df = pd.read_fwf(filename, colspecs=col_specs, names=col_names)

