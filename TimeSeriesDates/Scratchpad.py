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


# invalid data
pd.to_datetime(['2009/07/31', 'asd'], errors = 'raise') # raise error
pd.to_datetime(['2009/07/31', 'asd'], errors = 'ignore') # if unparseable,
# 	return array - don't actually parse
pd.to_datetime(['2009/07/31', 'asd'], errors = 'coerce') # I like this one,
# 	more similar to R - if you can't parse, just make into NA value, but
# 	keep everything else as expected


# epoch timestamps
# can convert integer / float to dates, default is nanoseconds, but you can
# 	specify the units and it still converts
pd.to_datetime(
	[1349720105, 1349806505, 1349892905,1349979305, 1350065705],
	unit='s'
)
pd.to_datetime(
	[1349720105100, 1349720105200, 1349720105300, 1349720105400, 1349720105500],
	unit='ms'
)
# these work but results unexpected
pd.to_datetime([1])
pd.to_datetime([1, 3.14], unit='s')


# make ranges of timestamps
dates = [
	datetime.datetime(2012, 5, 1),
	datetime.datetime(2012, 5, 2),
	datetime.datetime(2012, 5, 3)
]
index = pd.DatetimeIndex(dates) # freq = None
index = pd.Index(dates) # coered into dt index
# make indexes, use functions
index = pd.date_range('2000-1-1', periods = 1000, freq = 'M') # 1000 months...
index = pd.bdate_range('2012-1-1', periods = 250) # default freq is 1 day
index = pd.date_range('2012-1-1', periods = 250, freq = 'D') # default freq
# 	is 1 day. THIS IS CALENDAR DAY, NOT BUSINESS DAY.
index = pd.date_range('2012-1-1', periods = 250, freq = 'B')
# 'B' FREQ IS BUSINESS DAY! SO YOU CAN QUICKLY MAKE AN INDEX OF BUSINESS
# 	DAYS OVER SOME TIME INTERVAL.
start = datetime.datetime(2011, 1, 1)
end = datetime.datetime(2012, 1, 1)
rng = pd.date_range(start, end) # can make using date_range
rng = pd.bdate_range(start, end)
pd.date_range(start, end, freq = 'BM')
pd.date_range(start, end, freq = 'W') # could use for weekly ot, weekly ix
pd.bdate_range(end = end, periods = 20) # goes back 20 periods from end
pd.bdate_range(start = start, periods = 20) # goes forwards 20 periods from
# 	start


# timestamp limitations - can't work with datetimes outside of these boundaries
pd.Timestamp.min
pd.Timestamp.max


# datetime index
# caution: not required to sort datetime index, but can have unintended 
# 	results if operating without sorting
rng = pd.date_range(start, end, freq = 'BM')
ts = pd.Series(np.random.randn(len(rng)), index = rng)
ts.index
ts[:5].index
ts[::2].index


# partial string matching
ts['1/31/2011'] # subset an object indexed with datetime index based on
# 	string representation of the date
ts['10/31/2011':'12/31/2011'] # slice using string rep
ts['2011'] # slice the year. this is pretty cool
ts['2011-6'] # slice by year month
dft = pd.DataFrame(
	np.random.randn(100000, 1),
  columns = ['A'],
  index = pd.date_range('20130101', periods = 100000, freq = 'T')
)
dft['2013'] # partial string date subsetting works on dfs too
dft['2013-1':'2013-2'] # includes start and end of months
dft['2013-1':'2013-2-28'] # goes up thru very end of 2/28 - up to 11:59:59 PM
dft['2013-1':'2013-2-28 00:00:00'] # specify stop time
dft['2013-1-15':'2013-1-15 12:30:00'] # stop time included

dft2 = pd.DataFrame(
	np.random.randn(20, 1),
	columns=['A'],
	index=pd.MultiIndex.from_product([
		pd.date_range('20130101',	periods=10,	freq='12H'), ['a', 'b']
	])
) # can throw dts into multiix
dft2.loc['2013-01-05 00:00:00'] # works, but
dft2.loc['2013-01-05'] # none of these work...
dft2.loc['2013-1-5']
dft2.loc['2013-01']
dft2.loc['2013-1']

dft2.loc['a'] # also, why doesn't this work?
dft2.loc['b', :]
dft2.loc['a', :]
dft2.loc[('a', '2013-01-05'), :]
dft2.loc['2013-01-05', :]
dft2.loc[('a', '2013-01'), :]
dft2.loc[('a', '2013-1'), :] # just pulls the first within that group,
# 	doesn't slice the entire group? seems like it should return the whole
# 	group.
dft2.loc[('b', '2013'), :] # this doesn't work at all how it should?

idx = pd.IndexSlice
dft2 = dft2.swaplevel(0, 1).sort_index() # swap the levels in the ix, then re sort
dft2.loc[idx[:, '2013-01-05'], :]
dft2.loc[pd.IndexSlice[:, 'a'], :] # THIS pulls the whole group for a
dft2.loc[pd.IndexSlice[:, 'b'], :] # works how i expect it to
dft2.loc[pd.IndexSlice['2013-01-04', :], :]
dft2.loc[pd.IndexSlice['2013-01-04', 'a'], :] # no idea why returns first only


# datetime indexing
# indexing with datetime objects is exact, while string matching is less so
# also include both endpoints
# datetime objects have specific hours, minutes, and seconds. if not
# 	explicity specified, they're 0
dft[datetime.datetime(2013, 1, 1):datetime.datetime(2013, 2, 28)]
dft[datetime.datetime(2013, 1, 1):datetime.datetime(2013, 1, 5)] # much better...?
dft[
	datetime.datetime(2013, 1, 1, 10, 12, 0):datetime.datetime(2013, 1, 5, 10, 12, 0)
] # so exact


# truncating and fancy indexing
# truncate is convenience function equiv to slicing
ts.truncate(before = '10/31/2011', after = '12/31/2011') # throw out anything
# 	before 10/31 and anything after 12/31
ts[[0, 5, 6]].index # ambiguous subsetting still ouputs datetime ix


# time/date components
x.weekday_name # in documentation, why not in module?


# DateOffset objects
# different increments in date sequences
# implementation similar to:
from pandas.tseries.offsets import * # have to import offsets separately
d = datetime.datetime(2008, 8, 18, 9, 0)
d + dateutil.relativedelta(months = 4, days = 5)
d + pd.DateOffset(months = 4, days = 5) # add 4 months and 5 days to d
# can use to add / subtract from a datetime object; 
# 	can multiply this by some integer;
# 	can rollforwards or rollback to an offset date
# apply() within DateOffset subclasses have custom date increment logic
class BDay(DateOffset):
	"""DateOffset increments between business days"""
	def apply(self, other):
		...
d - 5 * BDay() # go back 5 business days
d + BMonthEnd() # move forward to month end

# rollforward and rollback
d
offset = BMonthEnd()
offset.rollforward(d) # rolls forward to month end
offset.rollback(d) # back to month end of month right before
# THESE METHODS PRESERVE THE HOUR, MINUTE, SECOND, ETC. OF THE TIME YOU'RE
# 	ROLLING.
day = Day()
day.apply(pd.Timestamp('2014-01-01 09:00')) # add a day?
day = Day(normalize = True)
day.apply(pd.Timestamp('2014-01-01 09:00')) # add a day, reset the time to zero
hour = Hour()
hour.apply(pd.Timestamp('2014-01-01 22:00'))
hour = Hour(normalize = True)
hour.apply(pd.Timestamp('2014-01-01 22:00')) # resets to floor of date, no time
hour.apply(pd.Timestamp('2014-01-01 23:00')) # no idea why this goes forwards...


# parametric offsets
d
d + Week()
d + Week(weekday = 4) # goes up one week to the nearest Wednesday
(d + Week(weekday = 4)).weekday()
d - Week()
d + Week(normalize = True) # throws out hours, reset to zero
d - Week(normalize = True) # ""
# parameterizing YearEnd with ending month
d + YearEnd()
d + YearEnd(month = 6) # goes forward to year end, then adds 6 months




== STOPPED HERE ============================================
	Using offsets with Series / DatetimeIndex
	Offsets can be used with either a Series or DatetimeIndex to apply the offset to each element.


# Might be useful to go back and forth between datetime.datetime() and
# 	Timestamp objects
to_pydatetime

