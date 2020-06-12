from datetime import datetime, timezone, tzinfo, timedelta
from dateutil import tz
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters


register_matplotlib_converters()

locale = tz.gettz("America/Los_Angeles")
start = datetime(2020, 6, 10, 18, 0, 0, tzinfo=timezone.utc)
end = datetime(2020, 6, 10, 19, 0, 0, tzinfo=timezone.utc)
cartUrl = "/services/printing/Cart"
timeCol = "log_datetime"
timeTakenCol = "time-taken"
df = pd.read_csv("u_ex200611.data", sep="\s+", header=0,
                 parse_dates=True, infer_datetime_format=True)
df[timeCol] = pd.to_datetime(
    df["date"] + " " + df["time"], format="%Y%m%d %H:%M:%S", utc=True)

urlGroup = df.groupby(["cs-uri-stem"])

filt = (df["cs-uri-stem"] == cartUrl) & (df[timeCol]
                                         >= start) & (df[timeCol] < end)

total = df[filt][timeTakenCol].count()

filt = filt & (df[timeTakenCol] > 120000)
x = np.vectorize(lambda t: t.astimezone(locale))(df[filt][timeCol].to_numpy())
y = df[filt][timeTakenCol]
longRun = y.count()
print("{:.4%}".format(longRun/total))
