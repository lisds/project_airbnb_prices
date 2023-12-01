import numpy as np

rng = np.random.default_rng()

import pandas as pd

pd.set_option('mode.copy_on_write', True)

data = pd.read_csv('data/clean_df.csv')
data