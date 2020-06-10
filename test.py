from datetime import datetime, timezone, tzinfo, timedelta
from dateutil import tz
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters


register_matplotlib_converters()

locale = tz.gettz("America/Los_Angeles")
cartUrl = "/services/printing/Cart"
timeCol = "log_datetime"
timeTakenCol = "time-taken"
df = pd.read_csv("u_ex200610.log", sep="\s+", header=0,
                 parse_dates=True, infer_datetime_format=True)
df[timeCol] = pd.to_datetime(
    df["date"] + " " + df["time"], format="%Y%m%d %H:%M:%S", utc=True)

cart = df[df["cs-uri-stem"] ==
          cartUrl]
total = cart[timeTakenCol].count()

filt = (df["cs-uri-stem"] == cartUrl
        ) & (df[timeTakenCol] > 300000)
x = np.vectorize(lambda t: t.astimezone(locale))(df[filt][timeCol].to_numpy())
y = df[filt][timeTakenCol]
longRun = y.count()
print("{:.4%}".format(longRun/total))
plt.plot(x, y, "go")
plt.show()
