

df = DataFrame({
	'A' : ['foo', 'bar', 'foo', 'bar', 'foo', 'bar', 'foo', 'foo'],
	'B' : ['one', 'one', 'two', 'three', 'two', 'two', 'one', 'three'],
	'C' : random.randn(8),
	'D' : random.randn(8)
})

# splits data frame by rows
lst = [1, 2, 3, 1, 2, 3]
s = Series([1, 2, 3, 10, 20, 30], lst)

grouped = df.groupby(df['A'])
grouped = df.groupby(df['A', 'B'])

# splits data frame by columns
def get_letter_type(letter):
	if letter.lower() in 'aeiou':
		return('vowel')
	else:
		return('consonant')

grouped = df.groupby(get_letter_type, axis = 1)
# So you'd map out which columns here, then assign them to groups.
# axis specifies by column or by row
def get_type(letter):
	x = dtype(df[letter])
	return(x)
grouped = df.groupby(get_type, axis = 1)
grouped.first() # return a df of the left-most columns in each group
grouped.last() # return a df of the right-most columns in each group
grouped.get_group(dtype('O')).sum() # concatenate all string cols
# So this would be kinda like vapply(df, mode, character(1)) to map modes to columns

== look up groupby object methods / attributes ==
grouped = s.groupby(level = 0)
grouped.first() # return first element in each group
grouped.last() # return last element in each group
grouped.sum() # return sum of each group


values = Series([1, 1, 1, 1, 1, 1])
groups = ['A', 'A', 'A', 'B', 'B', 'C']
grouped = values.groupby(groups)
grouped.first()
grouped.last()
grouped.sum() # kinda like tapply()

df3 = DataFrame({ 'X' : ['A', 'B', 'A', 'B'], 'Y' : [1, 4, 3, 2]})
df3.groupby(['X']).get_group('A')

df.groupby('A').groups # Dictionary of the groups and thier corresponding indexes
df.groupby(get_letter_type, axis = 1).groups

== you can use tab complete on groupby object to view methods, super useful ==
grouped.head()
grouped.dtypes()
grouped.indices()
grouped.ngroups()
grouped.filter() # don't know what this means, prob useful
grouped.apply() # LIKE DDPLY VAPPLY; apply function to each group, either simplify into Series or keep as dataframe, probs some options for peicing everything back together





== groupby with multiindex ==
arrays = [['bar', 'bar', 'baz', 'baz', 'foo', 'foo', 'qux', 'qux'],
		  ['one', 'two', 'one', 'two', 'one', 'two', 'one', 'two']]
index = MultiIndex.from_arrays(arrays, names = ['first', 'second'])
s = Series(random.randn(8), index = index)
# So the multiindex is the array; the names of each index within the multiindex are first and second
# ; you're making a Series of random numbers; then you assign the multiindex to the Series of numbers
# so you can reason about it, work with the groups, etc.
arrays = [['male', 'male', 'female', 'female', 'female'],
 		  ['white', 'black', 'white', 'white', 'black']]
ix = MultiIndex.from_arrays(arrays, names = ['first', 'second'])
x = Series(random.randn(5), index = ix)

grouped = s.groupby(level = 0) # level arg is for which level / order of the multiindex you want to group by
s
grouped.first()
grouped.last() # note that this is the first index of the two in the multiindex
grouped = s.groupby(level = 1) # now on the second index of the two in the multiindex
s
grouped.first()
grouped.last()
grouped = s.groupby(level = 'second') # alternate syntax
grouped.first()



# group, then make different colluns - so you can only gropu it once, then manipulated separately
grouped = df.groupby(['A'])
grouped_C = grouped['C']
grouped_D = grouped['D']
# same as
df['C'].groupby(df['A']) # gropu one column by another
g_ser = Series([1, 1, 1, 1]).groupby(Series(['A', 'A', 'A', 'B'])) # again, grouping one by another. you don't need to do get indices with work, just group, then pull the indices attribute.
for name, group in g_ser:
	print(name)
	print(group)

# iterating through a grouped df
grouped = df.groupby('A')
for name, group in grouped:
	print(name)
	print(group)
	print(group[:1])
# iterate thru multiple keys
for name, group in df.groupby(['A', 'B']):
	print(name)
	print(group)

# get multiple gropus with tuple
df.groupby(['A', 'B']).get_group(('bar', 'one'))
df.groupby(['A', 'B']).get_group(('foo', 'two'))


# aggregate is method for grouped df objects
grouped = df.groupby('A')
grouped.aggregate(sum)
grouped = df.groupby(['A', 'B'])
grouped.aggregate(sum)
# group output over multiple keys returns a multiindexed data frame
grouped = df.groupby(['A', 'B'], as_index = False)
yay = grouped.aggregate(sum) # this was such a headache before; you don't NEED to have group output return a multiindex!
df.groupby('A', as_index = False).sum()
# reset_index() makes a new index, turning the existing index into columns. Alternate to groupby(<>, as_index = False)
df.groupby(['A', 'B']).sum().reset_index()

# size of each group, either length() for a Series or nrow() for a df
df.groupby(['A', 'B']).size()
s.groupby(level = 0).size()

# looks like pd.Series functions like a R list - general purpose container witih iteration
x = Series([Series(['A', 'B']), True, [1, 2]])
x[0]
x[1]
x[2]

# pass multiple functions to groups
grouped = df.groupby('A')
grouped['C'].agg([sum, mean, std]) # this is basically dplyr::group_by + dplyr::summarize
s.groupby(level = 0).agg([sum, mean, min, max]) # summary table out of a series
# passing a dict means that you can name the output columns
df.groupby('A', as_index = False)['C'].agg({
	'Var.Sum' : sum,
	'Var.Mean' : mean,
	'Var.Min' : min,
	'Var.Max' : max
}) # this is so ridiculously similar to dplyr / plyr that I don't know why plyr is so famous...
# apply grouping and functions TO EACH (non-group / index) COLUMn
grouped.agg([sum, mean, std])
grouped.agg([sum, mean, std]).reset_index() # looks like multiindex can be on columns too

# passing a dict to apply different aggregation functions to columns
grouped.agg({'C' : sum, 'D' : lambda x: std(x, ddof=1)}) # keys have to be col names because output is by column this way
# access functions by string
grouped.agg({'C':'sum','D':'std'})

# common aggregation functions are super optimized
df.groupby('A').sum()
df.groupby(['A', 'B']).mean()


# TRANSFORMation
# returns an output object that is the same size as the grouped input object
# Wondering if this is similar to ave(), in that it applies a function but output is same size as input (i.e. doesn't shorten to number of groups)
index = date_range('10/1/1999', periods=1100)
ts = Series(random.normal(0.5, 2, 1100), index)
ts = ts.rolling(window=100,min_periods=100).mean().dropna() # not sure what rolling() method is??? like zoo::rollaply? or a rolling apply, defined with lapply or vapply?? it'd make sense for this to be implemente in th ebase package...
ts.head()
ts.tail()
key = lambda x: x.year
zscore = lambda x: (x - x.mean()) / x.std()
transformed = ts.groupby(key).transform(zscore)
# So this computes the sum for each group, then replaces each input value with the sum of that group
sf = Series([1, 1, 2, 3, 3, 3])
sf.groupby(sf).transform(sum)
df = DataFrame({ 'vals' : sf, 'groups' : Series(['A', 'B', 'A', 'C', 'C', 'C'])})
df.groupby('groups').transform(sum)
df.groupby('groups').transform(cumsum) # this is ave(vect, groups, FUN = cumsum)
# so aggregate collapses the output by group - returns one output per group, while transform returns
# 	the group output for each element belonging to each group.
s.groupby(level = 0).transform(sum)
s.groupby(level = 0).aggregate(sum)

# window.Rolling
ts_roll = ts.rolling(window = 5) # define the rolling object
ts_roll.min()
ts_roll.max()
ts_roll.mean() # then apply tons of rolling functions to that object

== tons of tranformation stuff ==

data_df = pd.DataFrame(np.random.randn(10, 3), columns = ['A', 'B', 'C'])
data_df.where(~(data_df < -0.50), np.nan, inplace = True)
countries = np.array(['US', 'UK', 'GR', 'JP'])
key = countries[np.random.randint(0, 4, data_df.shape[0])]
grouped = data_df.groupby(key)
grouped.count()
	# Intermezzo:
	data_df.fillna(999) # fill nas in object
	data_df.mean() # can do colwise or rowwise means via axis argument
	data_df.fillna(data_df.mean())
f = lambda x: x.fillna(x.mean()) # f(pd.Series([1, np.nan, 3]))
transformed = grouped.transform(f)
# So here, you're grouping the data frame by country; making an anonymous
# 	function for filling a series or dataframe nas with a mean; then calling
# 	the anon function on the data for every country, while maintaining the
# 	same number of rows and cols. (not sure why this has to be transform and
# 	can't be apply?)
data_df.index = key
data_df.sort_index(inplace = True)
gpd = data_df.groupby(level = 0)

f(gpd.get_group('US')) # at group level, so split apply combine
transd = gpd.transform(f) # output has same indexes as input
applied = gpd.apply(f) # is it trying to call f() on the whole df?? # not sure why apply doesn't work...
gpd.apply(lambda x: x.iloc[0, 0])
gpd.apply(lambda x: f(x)) 

data_df['Key'] = key
gpd = data_df.groupby('Key')
transd = gpd.transform(f)
applied = gpd.apply(f) # still no idea why this doesn't work. Might be
# 	because transform() has a mandate to keep original shape, and apply
# 	doesn't - so maybe apply() is trying to simplfy the results here, hence
# 	the shape error. Might be worth checking output from f() on each group
# 	to pinpoint the error.
group1 = gpd.get_group(list(gpd.groups.keys())[0])
group2 = gpd.get_group(list(gpd.groups.keys())[1])
group3 = gpd.get_group(list(gpd.groups.keys())[2])
group4 = gpd.get_group(list(gpd.groups.keys())[3])
group1
f(group1) # same shape
group2
f(group2) # same shape
group3
f(group3) # same shape
group4
f(group4) # same shape
# This didn't work...



# FILTRATION
sf = pd.Series([1, 1, 2, 3, 3, 3])
sf.groupby(sf).filter(lambda x: x.sum() > 2) # filters out observations in the series where the sum for the whole gropu is over 2
sf.groupby(sf) # is a clean way of breaking a series up into groups based on unique values
# group wise filtering


dff = pd.DataFrame({'A': np.arange(8), 'B': list('aabbbbcc')})
dff.groupby('B').filter(lambda x: len(x) > 2) # throw out groups where the
# 	group is less than 2 obs.
dff['C'] = np.arange(8)
dff.groupby('B').filter(lambda x: len(x['C']) > 2) # if multiple columns,
# 	you need to specify the one you're using for filtering.

grouped = df.groupby('A')

tsdf = pd.DataFrame(
	np.random.randn(1000, 3),
	index=pd.date_range('1/1/2000', periods=1000),
	columns=['A', 'B', 'C']
)
tsdf.ix[::2] = np.nan
grouped = tsdf.groupby(lambda x: x.year)
grouped.fillna(method='pad') # fill in nas from adjacent rows


s = pd.Series([9, 8, 7, 5, 19, 1, 4.2, 3.3])
g = pd.Series(list('abababab'))
gb = s.groupby(g)
gb.nsmallest(3)
gb.nlargest(3)


df = pd.DataFrame({
	'A' : ['foo', 'bar', 'foo', 'bar', 'foo', 'bar', 'foo', 'foo'],
	'B' : ['one', 'one', 'two', 'three', 'two', 'two', 'one', 'three'],
	'C' : np.random.randn(8),
	'D' : np.random.randn(8)
})
grouped = df.groupby('A')
grouped['C'].apply(lambda x: x.describe())
# call describe() on groups defined by 'C' column
grouped = df.groupby('A')['C']
def f(group):
	return pd.DataFrame({
		'original' : group, 'demeaned' : group - group.mean()
	})
grouped.apply(f)

def f(x):
	return pd.Series([ x, x**2 ], index = ['x', 'x^2'])
s
s.apply(f)
# split apply combine on a series, then upcast into a data frame.
# apply() can be a reducer, transformer, or filter, depending on what you
# 	pass.

df.groupby('A').std()
# 'nuisance' columns are dropped ('B' here because you didn't group by it)

data = pd.Series(np.random.randn(100))
factor = pd.qcut(data, [0, .25, .5, .75, 1.])
data.groupby(factor).mean()
# order of levels preseved if grouping key is categorical object
# this data type is crazy; the factor label is a range of floats


# more specific grouping ways
import datetime
df = pd.DataFrame({
	'Branch' : 'A A A A A A A B'.split(),
	'Buyer': 'Carl Mark Carl Carl Joe Joe Joe Carl'.split(),
	'Quantity': [1,3,5,1,8,1,9,3],
	'Date' : [
		datetime.datetime(2013,1,1,13,0),
		datetime.datetime(2013,1,1,13,5),
		datetime.datetime(2013,10,1,20,0),
		datetime.datetime(2013,10,2,10,0),
		datetime.datetime(2013,10,1,20,0),
		datetime.datetime(2013,10,2,10,0),
		datetime.datetime(2013,12,2,12,0),
		datetime.datetime(2013,12,2,14,0),
	]
})
df.groupby([pd.Grouper(freq = '1M', key = 'Date'), 'Buyer']).sum()
# looks like you can group the data first by month - '1M' within the 'Date'
# 	field, then by 'Buyer'; then take the sum
df = df.set_index('Date')
df['Date'] = df.index + pd.offsets.MonthEnd(2) # something like go back a
# 	month within the index
df.groupby([pd.Grouper(freq='6M',key='Date'),'Buyer']).sum() # every 6
# 	months. this uses the Date field
df.groupby([pd.Grouper(freq='6M',level='Date'),'Buyer']).sum() # still every
# 	6 months, but uses index which is date, but adjusted for something.


# taking first rows of each group
df = pd.DataFrame([[1, 2], [1, 4], [5, 6]], columns=['A', 'B'])
g = df.groupby('A')
g.head(1) # just spec the number of rows you want using head / tail
g.tail(1)

# take nth row of each group
df = pd.DataFrame([[1, np.nan], [1, 4], [5, 6]], columns=['A', 'B'])
g = df.groupby('A')
g.nth(0)
g.nth(-1) # starts going backwards, so len(x) - 1
g.nth(1) # drops '5', which doesn't have anything at ix[1]
g.nth(0, dropna = 'any') # throws out NA
g.first() # gets first non-na value / drops nas, then gets first value
g.nth(-1, dropna = 'any')
g.last()
g.B.nth(0, dropna=True) # gets column by, grouped by column A

df = pd.DataFrame([[1, np.nan], [1, 4], [5, 6]], columns=['A', 'B'])
g = df.groupby('A',as_index=False)
g.nth(0)
g.nth(-1)
# if you don't group by index, it won't throw out Na values


business_dates = pd.date_range(start='4/1/2014', end='6/30/2014', freq='B')
df = pd.DataFrame(1, index=business_dates, columns=['a', 'b'])
df.groupby((df.index.year, df.index.month)).nth([0, 3, -1])
# take the first, 4th, and second to last from every year-month combindation


df = pd.DataFrame(list('aaabba'), columns=['A'])
df

df.groupby('A').cumcount() # this'd be great for consec days worked in week.
df.groupby('A').cumcount(ascending=False)  # order in which each appears
# 	within the group


np.random.seed(1234)
df = pd.DataFrame(np.random.randn(50, 2))
df['g'] = np.random.choice(['A', 'B'], size=50)
df.loc[df['g'] == 'B', 1] += 3
df.groupby('g').boxplot()


# regrouping by factor
df = pd.DataFrame({'a':[1,0,0], 'b':[0,1,0], 'c':[1,0,0], 'd':[2,3,4]})
df.groupby(df.sum(), axis=1).sum()
# rowsums for column groups; two groups are columsn that sum to one or
# 	that sum to 9.


df = pd.DataFrame({
	'a':  [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2],
	'b':  [0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1],
	'c':  [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
	'd':  [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
})
def compute_metrics(x):
	result = {'b_sum': x['b'].sum(), 'c_mean': x['c'].mean()}
	return pd.Series(result, name = 'metrics')
result = df.groupby('a').apply(compute_metrics)
# returning a names series for each group chunk allows you to peice output
# 	into data frame; useful for stacking.

pd.Series({'first': 1, 'second': 2}) # didn't know you could have named
# 	series


