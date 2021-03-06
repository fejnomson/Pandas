



== indexing and selecting data =================================================
http://pandas.pydata.org/pandas-docs/stable/indexing.html



dates = pd.date_range('1/1/2000', periods=8)
df = pd.DataFrame(np.random.randn(8, 4), index=dates, columns=['A', 'B', 'C', 'D'])
df

panel = pd.Panel({'one' : df, 'two' : df - df.mean()})
panel

s = df['A']
s[dates[5]]

df[['B', 'A']] = df[['A', 'B']] # can be good for transforming certain columns. but might be better to use .groupby(axis = 1)? group cols and apply by group?
df[['A', 'B']] = df[['A', 'B']].apply(pd.to_numeric)
df[['A', 'B']] = df[['A', 'B']].astype(float)
# convert cols just like in R... ?
string_cols = ['A', 'B']
df[string_cols] = df[string_cols].astype(str)
df[string_cols] = df[string_cols].astype(str)
# Alternate
df = pd.DataFrame(np.random.randn(8, 4), index=dates, columns=['A', 'B', 'C', 'D'])
df[string_cols] = df[string_cols].apply(lambda x: pd.Series(str(x))) # have no idea why this doesn't work
df[string_cols] = df[string_cols].apply(str) # looks like this might call str on the whole data frame, or something similar
df[string_cols] = df[string_cols].apply(pd.to_numeric) # but this works


# I think np.array is the preferred structure for subsetting
sa.ix[np.array([False, True, False])]
# Can convert np.array from pd.Series is ok:
sa.iloc[np.array(pd.Series([False, True, False])) # integer subsetting
sa.loc[np.array(pd.Series([False, True, False]))] # label subsetting
sa.ix[np.array(pd.Series([False, True, False]))] # either subsetting

# Subsetting with pd.Series won't work
sa.ix[pd.Series([False, True, False])]
# Unless the index matches with what you're subsetting
sa.ix[pd.Series([False, True, False], index = sa.index)]
# lists also work
sa.ix[[False, True, False]]

# indexes are attributes
sa = pd.Series([1,2,3], index=list('abc'))
dfa = df.copy()
sa.b # THIS IS CRAZY...
sa.b == sa['b']
dfa.A
dfa.B
panel.keys()
panel.one
# can use attributes for setting values, but CAN CREATE NEW ATTRIBUTE INSTEAD OF NEW COLUMN
sa.a = 5
sa
dfa.A = list(range(len(dfa.index))) # works BECAUSE A ATTRIBUTE IS ALREADY A COLUMN
dfa['A'] = list(range(len(dfa.index))) # this is preferred, won't fail silently

# selection by callable (anon function?)
df1 = pd.DataFrame(
	np.random.randn(6, 4),
	index=list('abcdef'),
	columns=list('ABCD')
)
df1.loc[lambda x: x.A > 0, :] # works in documentation, but not here?
df1.loc[lambda x: x['A'] > 0, :]
ix = np.array(df1['A'] > 0) # ix should be np.array
df1.loc[ix, :]

# optimised scalar value getting and setting; faster w/less overhead
s.iat[5] # integer subsetting
s.at[dates[5]] # label subsetting
sa.at['b']
df.at[dates[5], 'A']
df.iat[5, 0]
# like other indexing, you can set values:
df.at[dates[5], 'E'] = 999
df.iat[5, 4] = 000
# can enlarge objects using at:
df.at[dates[-1] + 1, 0] = 999
# but not iat:
df.iat[len(dates) + 2, len(df.columns)] = 999


# boolean indexing
s = pd.Series(range(-3, 4))
s[s > 0]
s[(s < -1) | (s > 0.5)]
s[~(s < 0)] # the not operator is ~, which is weird
df[df['A'] > 0]
# boolean indexing with list comprehensions and map method
df2 = pd.DataFrame({
	'a' : ['one', 'one', 'two', 'three', 'two', 'one', 'six'],
	'b' : ['x', 'y', 'y', 'x', 'y', 'x', 'x'],
	'c' : np.random.randn(7)
})
criterion = df2['a'].map(lambda x: x.startswith('t')) # kinda similar to lapply(df2['a'], function(x) startswith('t')) %>% unlist
# looks like <series>.map() is a way to call a function on EVERY ELEMNT in a
# 	series. You can't call <string>.startswith() on a non-scalar
df2[criterion] # i LOVE this. so R-like

keeps = pd.Series(['two', 'six'])
ix = df2['a'].map(lambda x: x.isin(keeps))
ix = df2['a'].map(lambda x: x in keeps)
ix = df2['a'].map(lambda x: keeps.isin([x]))
ix = df2['a'].map(lambda x: x.str.contains(keeps))
ix = df2['a'].map(lambda x: pd.Series([x]).isin(keeps)) # whatever. not figuring out how to make this scalar. map() could be great for the ix_vvply, vapply, etc. problems.
ix = df2['a'].isin(keeps) # df2[['a']] %in% keeps # doesn't work, but should?
df2[ix]
df2[df2['a'].isin(keeps)] # cleaner
df2.ix[df2['a'].isin(keeps)]
df2.loc[df2['a'].isin(keeps)]

'two'.str.contains(keeps)
keeps.str.contains('two')

df2[[x.startswith('t') for x in df2['a']]] # this is equivalent to the one below. (but slower)
df2['a'].map(lambda x: x.startswith('t'))

# multiple axis
df2.loc[criterion & (df2['b'] == 'x'), 'b':'c'] # accross multiple axis

# indexing with isin()
s = pd.Series(np.arange(5), index=np.arange(5)[::-1], dtype='int64')
s.isin([2, 4, 6])
s[s.isin([2, 4, 6])]
# can use on index objects
s[s.index.isin([2, 4, 6])] # restricts only to labels in index
s[[2, 4, 6]] # makes an NA, because you're assuming all labels present

s_mi = pd.Series(
	np.arange(6),
	index=pd.MultiIndex.from_product([[0, 1], ['a', 'b', 'c']])
)
s_mi.iloc[s_mi.index.isin(
	[
		(1, 'a'), # pull where s_mi.index.levels[0] == 1 & s_mi.index.levels[1] == 'a'
		(2, 'b'), # pull where s_mi.index.levels[0] == 2 & s_mi.index.levels[1] == 'b'. there's no '2' values in the first level, so this is dropped silently
		(0, 'c') # pull where s_mi.index.levels[0] == 0 & s_mi.index.levels[1] == 'c'
	]
)]
s_mi.iloc[s_mi.index.isin(['a', 'c', 'e'], level = 1)] # which elements of the index.levels[1] are in 'a', 'c', or 'e' - filter by only one level of the multiindex
# dataframe indexing with isin()
df = pd.DataFrame({
	'vals': [1, 2, 3, 4],
	'ids': ['a', 'b', 'f', 'n'],
	'ids2': ['a', 'n', 'c', 'n']
})
values = ['a', 'b', 1, 3]
df.isin(values) # so it tests EVERY cell in df for inclusion in values list
df[df.isin(values)] # note that this keeps full NA rows if not included
df[df.isin(values)].dropna(axis = 0, how = 'all') # drop if entire row is NAN
df[df.isin(values)].dropna(axis = 1, how = 'all') # drop if entire column is NaN


# match certain values with certain columns
values = {
	# each key is a column, and each value is a list of values you want to
	# 	check inclusiveness for
	'ids': ['a', 'b'],
	'vals': [1, 3]
}
df.isin(values)
# try 2 get same rows in each column
values = {
	'ids' : ['f'],
	'ids2' : ['c'],
	'vals' : [3]
}
df.isin(values)
df[df.isin(values)]

# any() and all()
values = {
	'ids': ['a', 'b'],
	'ids2': ['a', 'c'],
	'vals': [1, 3]
}
row_mask = df.isin(values).all(1) # all(axis = 0) for row ix, all(axis = 1) for columns
# the call to .all(1) means: only return rows where every row is True
# .all(0) is cols where every value is True
# row_mask is a boolean Series of which rows are all true in df.isin(values)
df[row_mask] # returns data frame where rows are all true from
# 	df.isin(values).
col_mask = df.isin(values).all(0)
df.loc[:, col_mask] # must call .loc() method because you're not going
# 	directly for rows or labels.


# where() method and masking: to guarantee that selection output is same
# 	shape as data you're selecting from
s
s[s > 0]
len(s)
len(s[s > 0])
s.where(s > 0)
len(s.where(s > 0))

df = pd.DataFrame(
	# np.array() is preferred object for making dfs
	np.random.randn(8, 4),
	index=dates,
	columns=['A', 'B', 'C', 'D']
)
mydict = {
	# So pd.DataFrame() takes in a dictinary object, where the keys are turned
	# 	into column names and the values are turned into pd.Series() objects.
	# Additionals
	'A': np.random.randn(4),
	'B': np.random.randn(4),
	'C': np.random.randn(4),
	'D': np.random.randn(4),
}
df = pd.DataFrame(mydict)

df[df < 0 ] # VERY similar to R; filters via every value in df
df.where(df < 0) # This is the implementatino of the above; the where() is
# 	used to maintain the NA values - to avoid throwing out the values that
# 	don't pass the test.
df.where(df < 0, 999) # where() takes an argument to specify the replacement
# 	value if the expression evaluates to False. So anything that ISN'T less
# 	than zero is replaced with 999 here.
df.where(df < 0, df - 999)
# this is very similar to ifelse(<expression>, <keep value>, <replacement>)
df2 = pd.DataFrame({
	'A': np.repeat(1, 4),
	'B': np.repeat(2, 4),
	'C': np.repeat(3, 4),
	'D': np.repeat(4, 4)
})
df.where(df < 0, df2) # can assign elements from one data frame to another
# 	where some condition is met. Wondering if this is kinda like matrix
# 	operations are handled in R - flattened into one long vector, then you
# 	iterate through, then bind it back together into its original shape
df.where(df < 0, other = df2, inplace = True) # THIS IS INSANE!!! MODIFY IN
# 	PLACE?? AVOID COPYING EVERYTHING, ALL THE TIME, NO MATTER WHAT?
# There's also axis and levels args, not experimenting with them for now


# Set value based on boolean vals
s2 = s.copy()
s2[s2 == 3] = 999 # Love this.
df2 = df.copy()
df2[df2 < 0] = 'jeff' # amazing.
# alignment
df2 = df.copy()
ix = df2[1:4] > 0 # data frame of bools, kinda like ix but 2 dimensional.
# 	Subsets to rows 1:3, I think based on index; then tests every value for
# 	being > 0.
df2[ix] = 3

# axis and level arguments
df = pd.DataFrame({
	'A': np.array([1, 2, 3, 4]),
	'B': np.repeat(0, 4),
	'C': np.repeat(0, 4),
	'D': np.repeat(0, 4)
})
df2 = df.copy()
df2.where(df2 > 0, df2['A'], axis = 'index') # Think df2['A'] is other arg
df2.where(df2 > 0, df2['A'], axis = 0) # 'if df2[x, y] isn't > 3, replace it
# 	with the value from df2[x, df2.A[y]]'
df2.where(df2 == 0, df2['A'], axis = 0) # nothing changes here, because
# 	everything evaluates to True.
df2.where(df2 <= 0, df2.iloc[0], axis = 1) # Basically, if a value doesn't
# 	pass the x <= 0 test, swap that value with the one from the same column
# 	in the row you specified: if df[x, y] ~<= 0


to_rep_row = pd.Series([
	'Replaced - 0', 'Replaced - 1', 'Replaced - 2', 'Replaced - 3'
])
to_rep_col = pd.Series([
	'Replaced - 0', 'Replaced - 1', 'Replaced - 2', 'Replaced - 3'
])
df = pd.DataFrame({
	'A': range(0, 4),
	'B': range(4, 8),
	'C': range(8, 12),
	'D': range(12, 16)
})
df2 = df.copy()
df2.where(df2 % 2 == 0, to_rep_row, axis = 1) # not sure why this goes to nan. maybe, if you're going by row, it doens't want to reset the dtype of series, so it changes to nan when it sees that its a different dtype
df2.where(df2 % 2 != 0, to_rep_col, axis = 0) # but this works as expected...

# a slower, but equivalent version:
df3 = df.copy()
df.apply(lambda x, y: x.where(x > 10, y), y = df['A'])


# mask is the opposite of where:
df.where(df > 10)
df.mask(df > 10)

# where() accepts callables as condition AND other arg
df3 = pd.DataFrame({
	'A': [1, 2, 3],
	'B': [4, 5, 6],
	'C': [7, 8, 9]
})
df3.where(lambda x: x > 4, lambda x: x + 10) # guess this doesn't actually work...


# Duplicates
df2 = pd.DataFrame({
	'a': ['one', 'one', 'two', 'two', 'two', 'three', 'four'],
	'b': ['x', 'y', 'x', 'y', 'x', 'x', 'x'],
	'c': np.random.randn(7)
})
df2.duplicated('a') # first occurance kept, subsequent occurance thrown out
df2.duplicated('a', keep = 'first') # same; default
df2.duplicated('a', keep = 'last') # last occurance kept, each higher current occurance thrown out
df2.duplicated('a', keep = False) # marks duplicates for ENTIRE GROUP. So in
# 	c(1, 1, 2, 3, 3, 4), you'd identify c(1, 1, 3, 3) and c(2, 4). Throws
# 	out groups that have ANY duplicates in them.
df2.drop_duplicates('a') # sugar for df2.loc[df2.duplicated('a',keep='first')]
df2.drop_duplicates('a', keep = 'last')
df2.drop_duplicates('a', keep = False)
# multiple columns
df2.duplicated(['a', 'b'])
df2.drop_duplicates(['a', 'b'])
df2.drop_duplicates(['a', 'b', 'c'])
# by index
df3 = pd.DataFrame({
		'a': np.arange(6),
		'b': np.random.randn(6)
	},
	index = ['a', 'a', 'b', 'c', 'b', 'a']
)
df3.index.duplicated()
df3[~df3.index.duplicated()]

s = pd.Series([1,2,3], index=['a','b','c'])
s.get('a') # alternate subsetting by key/index
s.get('x', default = 'jeff') # if key is missing, you can supply default value


# select()
df.select(lambda x: x == 'A', axis = 1) # takes a function that operates on 
# 	labels accross an axis.
df.select(lambda x: x == 1, axis = 0)
df.select(lambda x: df[x].sum() < 7, axis = 1) # this is pretty sweet. filter
# 	df to columns where the sum of the column is < 7
df.select(lambda x: df[x].sum() >= 7, axis = 1)
df.select(lambda x: df.loc[x].sum() == 36, axis = 0) # go thru the index
# 	(rows), check for sum == 36, then subset to rows that meet that condition
df['Name'] = pd.Series(['jeff', 'jessica', 'solomon', 'jim'])
df.select(lambda x: df[x].dtype == 'int32', axis = 1) # love this
df.select(lambda x: df[x].dtype == 'object', axis = 1)

# lookup
dflookup = pd.DataFrame(
	np.random.rand(20,4),
	columns = ['A','B','C','D']
)
dflookup.lookup(list(range(0,10,2)), ['B','C','A','B','D']) # pull values
# 	given list of row label and col labels; output is a vect / numpy array


# index objects
index = pd.Index(['e', 'd', 'a', 'b'])
'd' in index
index = pd.Index(['e', 'd', 'a', 'b'], name = 'something')
index.name

index = pd.Index(list(range(5)), name = 'rows')
columns = pd.Index(['A', 'B', 'C'], name = 'cols')
df = pd.DataFrame(
	np.random.randn(5, 3),
	index = index,
	columns = columns
)

ind = pd.Index([1, 2, 3])
ind.rename('apple') # returns a copy, doensn't mod in place
ind.set_names(['apple'], inplace = True)
ind.name
ind.name = 'bob'

# set operations on index objects
a = pd.Index(['c', 'b', 'a'])
b = pd.Index(['c', 'e', 'd'])
a | b # union, unique vals
a & b # in both indexes
a.difference(b) # setdiff(a, b)
b.difference(a) # setdiff(b, a)
a.difference(b).union(b.difference(a)) # c(setdiff(a, b,), setdiff(b, a))
a.sym_diff(b) # sugar for above # c(setdiff(a, b,), setdiff(b, a))
a ^ b # ""

# missing values - try to avoid missing values in indexes
idx1 = pd.Index([1, np.nan, 3, 4])
idx1
idx1.fillna(2) # fillna na
idx2 = pd.DatetimeIndex([
	pd.Timestamp('2011-01-01'), pd.NaT, pd.Timestamp('2011-01-03')
])
idx2
idx2.fillna(pd.Timestamp('2011-01-02')) # returns copy

# set an index
df2
indexed1 = df2.set_index('a') # take a column in a df and set it as an index
indexed1
indexed2 = df2.set_index(['a', 'b']) # multiple columns to multiindex
indexed2 # this is basically the opposite of df.reset_index()
indexed2.reset_index()
frame = df2.set_index('a', drop = False) # keeps existing index
frame = frame.set_index(['a', 'b'], append = True) # still keeps existing index
df2.set_index('a', drop = False)
df2.set_index(['a', 'b'], inplace = True) # mod in place, don't append

# reset the index
frame.reset_index(level = 1) # reset part of the index -> bring one level of
# 	a multiindex into the df.
frame.reset_index(level = [1, 2])


# RETURNING VIEW VS. COPY
dfmi = pd.DataFrame(
	data = [
		list('abcd'),
		list('efgh'),
		list('ijkl'),
		list('mnop')
	],
	columns = pd.MultiIndex.from_product([
		['one','two'],
		['first','second']
	]),
	index = ['jeff', 'jessica', 'solomon', 'jim']
)
dfmi['one']['second'] # chained, same as:
first = dfmi['one'] # chained 1/1
first['second'] # chained 2/2
dfmi.loc[:, ('one', 'second')] # not chained; preferred
# the problem here is that, if youi're assigning values, you dont' know how
# 	pandas will assign it, unless you avoid chaining.
dfb = pd.DataFrame({
	'a' : ['one', 'one', 'two', 'three', 'two', 'one', 'six'],
	'c' : np.arange(7)
})
dfb['c'][dfb.a.str.startswith('o')] = 42 # This is never an issue in R...

dfc = pd.DataFrame({
	'A' : ['aaa','bbb','ccc'],
	'B' : [1,2,3]
})
dfc.loc[0, 'A'] = 11 # preferred value setting

dfc = dfc.copy()
dfc['A'][0] = 111 # result not guaranteed

dfc.loc[0]['A'] = 1111 # will never work



== SKIPPED: the QUERY() METHOD ==========================================
	DataFrame objects have a query() method that allows selection using an expression.


