http://pandas.pydata.org/pandas-docs/stable/timeseries.html



rng = pd.date_range('1/1/2011', periods = 72, freq = 'H')
rng[:5]
# make date time object. not sure why this is an index as opposed to a
# 	series?

ts = pd.Series(np.random.randn(len(rng)), index = rng)
# use as index

converted = ts.asfreq('45Min', method = 'pad')
# convert

# OVERVIEW OF DATE TIME TYPES
# 
# Timestamp
# single time stamp
# pd.to_datetime, Timestamp
#
# DatetimeIndex
# Timestamp, but as Index
# to_datetime, date_range, DatetimeIndex
#
# Period
# single time span. probably like duration (or period) in lubridate?
# period_range, PeriodIndex

import datetime as datetime

# Timestamp is probably the main datetime workhorse for pandas
pd.Timestamp(datetime.datetime(2012, 5, 1))
# looks pretty similar to posixct

pd.Period('2011-01') # makes a month-long period
pd.Period('2012-05', freq = 'D') # month long at daily resolution

# lists of timestamp and period automatically coerce into index
dates = [
	pd.Timestamp('2012-05-01'),
	pd.Timestamp('2012-05-02'),
	pd.Timestamp('2012-05-03')
] # but looks like this stays as a list?
ts = pd.Series(np.random.randn(3), dates) # coerced when you want it to be a list...
type(ts.index)
periods = [
	pd.Period('2012-01'),
	pd.Period('2012-02'),
	pd.Period('2012-03')
]
ts = pd.Series(np.random.randn(3), periods)
type(ts.index)
# I'm wondering if periods and indexes would be good for daily and weekly
# 	binning; e.g. have the index be the period, and all the data within that
# 	index falls within the period.


== STOPPED HERE ==
Converting to Timestamps
To convert a Series or list-like object of date-like objects e.g. strings, epochs, or a mixture, you can use the to_datetime function. When passed a Series, this returns a


