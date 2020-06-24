from datetime import datetime, timezone, tzinfo, timedelta
from dateutil import tz
import numpy as np
from scipy import stats
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters


register_matplotlib_converters()

locale = tz.gettz("America/Los_Angeles")
cartUrl = "/services/printing/Cart"
timeCol = "log_datetime"
timeTakenCol = "time-taken"
df = pd.read_csv("log_6_24.data", sep="\s+", header=0,
                 parse_dates=True, infer_datetime_format=True)
df[timeCol] = pd.to_datetime(
    df["date"] + " " + df["time"], format="%Y%m%d %H:%M:%S", utc=True)

filt = (df["cs-uri-stem"] == cartUrl) & (df["sc-status"] != 302)
cartInfo = df[filt][timeTakenCol]

total = cartInfo.count()
lessThan30Snd = cartInfo.loc[cartInfo < 30000].count()
lessThan1Min = cartInfo.loc[cartInfo < 60000].count()
lessThan2Min = cartInfo.loc[cartInfo < 120000].count()
lesshan5Min = cartInfo.loc[cartInfo < 300000].count()
gtrThan30Snd = lessThan1Min - lessThan30Snd
gtrThan1Min = lessThan2Min - lessThan1Min
gtrThan2Min = lesshan5Min - lessThan2Min
gtrThan5Min = total - lesshan5Min

print(f"From {df[timeCol].min()} to {df[timeCol].max()} with {total} requests")
print("{:.4%}".format(lessThan30Snd/total) + " take less than 30 seconds")
print("{:.4%}".format(gtrThan30Snd/total) +
      " take less than 1 minutes but more than 30 seconds")
print("{:.4%}".format(gtrThan1Min/total) +
      " take less than 2 minutes but more than 1 minutes")
print("{:.4%}".format(gtrThan2Min/total) +
      " take less than 5 minutes but more than 2 minutes")
print("{:.4%}".format(gtrThan5Min/total) + " take more than 5 minutes")
print("Mean of time taken:\t" + "{:,.0f} milliseconds".format(cartInfo.mean()))
print("Median of time taken:\t" +
      "{:,.0f} milliseconds".format(cartInfo.median()))
ax = cartInfo.hist(bins=100)
ax.set_title("Distribution of time taken")
ax.set_ylabel("Number of Request")
ax.set_xlabel("Time taken in milliseconds")
plt.show()
