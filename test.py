import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("u_ex200610.log", sep="\s+", header=0,
                 parse_dates=True, infer_datetime_format=True)
print(df)
