from cleaningdata import *

def meanfunc (column):
    variable = data_indexed[column]
    mean = variable.mean()
    return mean