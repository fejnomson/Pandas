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


# for converting to timestamp, use pd.to_datetime(); need a list like object
# 	of date-like objects
pd.to_datetime(pd.Series(['Jul 31, 2009', '2010-01-10', None]))
pd.to_datetime(['2005/11/23', '2010.12.31'])
pd.DatetimeIndex(
	['2005-11-23', '2010-12-31'],
	dtype = 'datetime64[ns]',
	freq = None
)
pd.to_datetime(['04-01-2012 10:00'], dayfirst = True) # dayfirst argument to specify if you want m d y or d m y
pd.to_datetime(['14-01-2012', '01-14-2012'], dayfirst = True) # IF A DATE
# 	CAN'T BE PARSED ACCORDING TO WHAT YOU SUPPLY WITH dayfirst, IT FALLS
# 	BACK ONTO THE NORMAL WAY; SO HERE, THERE'S NO 14 MONTH, SO EVEN THOUGH
# 	YOU SPECIFY DAYFIRST, IT'S FORCED INTO THINKING THAT 14 IS A DAY AND 1
# 	IS A MONTH. I don't think I like this - I think it's a little clearer to
# 	have one clear format that you specify and apply to all values in a
# 	container. Maybe an optional or default argument for having it guess the
# 	type before parsing, but I wouldn't have it be this flexible.
pd.to_datetime('1/9/2010', format = '%d/%m/%Y')
pd.to_datetime('1/9/2010', format = '%m/%d/%Y')
pd.to_datetime('1-9-2010', format = '%m-%d-%Y')
pd.to_datetime('1-9-2010', format = '%d-%m-%Y')
# Format arg takes the strftime for parsing times, which I like. Probs good
# 	to use this one explicity most of the time to avoid silent exceptions.

# So I think to_datetime converts something to Timestamp object, while 
# 	Timestamp instantiates a new timestamp object.
pd.to_datetime('2010/11/12')
pd.Timestamp('2010/11/12')

# can assemble from data frame
df = pd.DataFrame({
	'year': [2015, 2016],
	'month': [2, 3],
	'day': [4, 5],
	'hour': [2, 3]
})
pd.to_datetime(df) # this doesn't work...
pd.to_datetime(df[['year', 'month', 'day']])





== STOPPED HERE ==
Converting to Timestamps
To convert a Series or list-like object of date-like objects e.g. strings, epochs, or a mixture, you can use the to_datetime function. When passed a Series, this returns a
