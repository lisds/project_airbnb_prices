import numpy as np
import os

rng = np.random.default_rng()

import pandas as pd

pd.set_option('mode.copy_on_write', True)

script_dir = os.path.dirname('clean_df.csv')
full_path = os.path.join(script_dir, '../data/clean_df.csv')
data = pd.read_csv(full_path)

data_indexed = data.set_index('id')
data_indexed