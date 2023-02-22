import pandas as pd
import numpy as np


def get_validation_data_unseen(dataframe,validation_ratio=0.05,sample=False,sample_frac=0.1):
    if not sample:
        dataset = dataframe.copy()
    else:
        dataset = dataframe.sample(frac=sample_frac)
    data = dataset.sample(frac=(1-validation_ratio),random_state=48)
    unseen_data=dataset.drop(data.index)
    data.reset_index(inplace=True,drop=True)
    unseen_data.reset_index(inplace=True,drop=True)
    return data,unseen_data

    