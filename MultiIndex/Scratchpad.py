


# MultiIndex / Advanced Indexing
arrays = [['bar', 'bar', 'baz', 'baz', 'foo', 'foo', 'qux', 'qux'],
					['one', 'two', 'one', 'two', 'one', 'two', 'one', 'two']]
tuples = list(zip(*arrays))
index = pd.MultiIndex.from_tuples(tuples, names = ['first', 'second'])
index
# > MultiIndex(levels=[['bar', 'baz', 'foo', 'qux'], ['one', 'two']],
#            labels=[[0, 0, 1, 1, 2, 2, 3, 3], [0, 1, 0, 1, 0, 1, 0, 1]],
#            names=['first', 'second'])
s = pd.Series(np.random.randn(8), index = index)

# example for me
arrays = [
	['USA', 'USA', 'USA', 'CAN', 'CAN'],
	['IL', 'IL', 'NY', 'BC', 'ONT'],
	['Chicago', 'Oak Park', 'NYC', 'Vancouver', 'Ottowa']
]
tuples = list(zip(*arrays))
index = pd.MultiIndex.from_tuples(tuples, names = ['Country', 'State', 'City'])
s = pd.Series([8000000, 60000, 12000000, 600000, 1200000], index = index, name = 'Population')

# alternate way to make
index = pd.MultiIndex(
	levels = [
		['USA', 'CAN'], ['IL', 'NY', 'BC', 'ONT'], ['Chicago', 'Oak Park', 'NYC', 'Vancouver', 'Ottowa']
	],
	labels = [
		[0, 0, 0, 1, 1], [0, 0, 1, 2, 3], [0, 1, 2, 3, 4]
	],
	names = [
		'Country', 'State', 'Chicago'
	]
)
s = pd.Series([8000000, 60000, 12000000, 600000, 1200000], index = index, name = 'Population')

# alternate
iterables = [['bar', 'baz', 'foo', 'qux'], ['one', 'two']]
pd.MultiIndex.from_product(iterables, names = ['first', 'second'])
# alternate my example
# <didn't work: needs to be one per unique combination, similar to grid.expand()>

# can pass a list of arrays directly into Series or DataFrame to make multiix automatically:
arrays = [np.array(['bar', 'bar', 'baz', 'baz', 'foo', 'foo', 'qux', 'qux']),
					np.array(['one', 'two', 'one', 'two', 'one', 'two', 'one', 'two'])]
s = pd.Series(np.random.randn(8), index = arrays)
# my example:
arrays2 = [np.array(['USA', 'USA', 'USA', 'CAN', 'CAN']),
					np.array(['IL', 'IL', 'NY', 'BC', 'ONT']),
					np.array(['Chicago', 'Oak Park', 'NYC', 'Vancouver', 'Ottowa'])]
s = pd.Series([8000000, 60000, 12000000, 600000, 1200000], index = arrays2, name = 'Population')
# for dataframe, not series
df = pd.DataFrame(np.random.randn(8, 4), index = arrays)
# It's interesting that you can make ONE multiindex ONCE and then apply it to infinity vectors / dfs; e.g. maybe for grouping

# you can use the index on ANY AXIS OF A PANDAS OBJECT
df = pd.DataFrame(np.random.randn(3, 8), index = ['A', 'B', 'C'], columns = index)
df['bar']
df['bar']['one'] # so crazy
# So here, there are 8 columns and 8 combinations in the multiindex.
df = pd.DataFrame(np.random.randn(6, 6), index = index[:6], columns = index[:6])




== TOOK A DIVE INTO INDEXING / SUBSETTING, FOR BACKGROUND (COMES BEFORE MULTIINDEXING / ADVANCED INDEXING) ===========
df.loc[1, 1]
df.loc['bar', 'one']
df.iloc[1] # this is weird because it prints the row as a column. In r, it prints the row the same way that the dataframe prints
df.iloc[1, 1] # what you'd expect coming from R
df.iloc[0, 0]
df.iloc[, 0] # doesn't work like in R
df.loc['foo']
df.loc[['foo', 'bar']] # subset by label, using list of label levels
df.loc[['foo', 'bar']]['bar'] # subset rows by label, then cols by label
df.loc[['foo', 'bar']][['baz', 'foo']] # subset multiple rows and columns by label
df.iloc[[1, 3]] # subset rows by index; is what expected
df.iloc[pd.Series([1, 3])] # can use list or Series to subset, this is good becuase Series mimics some of the behavior of R data structure
df.loc[['foo', 'bar']]['bar']['one'] # subsetting gets really crazy when the row labels and column labels are multiindex
df.loc[('foo', 'one')] # subsets ROWS by 'foo' on key one and 'one' on key two
df.loc[('foo', 'one')][('bar', 'one')] # subsets rows by 'foo' on key one and 'one' on key two; subsets columns based on 'bar' on key one and 'one' on key too.
df.iloc[4, 0] # equivalent of above
df.loc[('foo', 'one'), ('bar', 'one')] # equivalent of above, much cleaner


x = pd.DataFrame({'x': [1, 2, 3], 'y': [3, 4, 5]})
x
x.iloc[1] = {'x': 999, 'y': 999} # can use dictionary to re-assign rows

s1 = pd.Series(np.random.randn(6),index=list('abcdef'))
# .loc for index-based subsetting
s1.loc['c':]
s1.loc['b']

df1 = pd.DataFrame(
	np.random.randn(6,4),
	index=list('abcdef'),
	columns=list('ABCD')
)
df1.loc['a'] > 0 # tests the first ROW, accessed by LABEL, for being > 0
df1['A'] > 0 # tests the first COLUMN, accessed by label, for being > 0
df1.iloc[:,1] # more similar to R: df[, 2]
df1.loc[:, df1.loc['a'] > 0] # return df1, but only columns where the first row is > 0


labs_keeps = pd.Series(['B', 'D'])
ix_keeps = pd.Series(df1.columns, index = df1.columns).isin(labs_keeps) # don't use # ix_keeps = pd.Series(df1.columns.values).isin(labs_keeps)
# so df1.columns is an INDEX. This makes sense because indexes are generally
# 	used for mapping out rows and columns. If you get the values, then it
# 	simplifies an order to np.array, which is a building block of an index.
# The point here is that when subsetting, .loc() uses the Index in ix_keeps
# 	or labs_keeps to match the value to the right column. If you just have a
# 	Series of booleans, .loc() doesn't know which value maps to which
# 	columns. If you assign the the columns Index to the boolean Index, then
# 	it knows where to map.
df1.loc[:, ix_keeps] # you CAN'T subset with a boolean, at least using .loc, which is weird
df1.loc[:, labs_keeps] # so you can just put a vector of field names in
# Further:
x = df1.loc['a'] > 0 # this boolean series keeps the column labels as the index
x.index
ix_keeps # but this one doesn't
ix_keeps.index

s = pd.Series(range(-3, 4))
s[s > 0]
s[(s < -1) | (s > 0.5)]
== TOOK A DIVE INTO INDEXING / SUBSETTING, FOR BACKGROUND (COMES BEFORE MULTIINDEXING / ADVANCED INDEXING) ===========



== STOPPED MULTIINDEXING DOCUMENTATION HERE: so search for this text to get started again ============================
	"This index can back any axis of a pandas object, and the number of levels of the index is up to you:"
http://pandas.pydata.org/pandas-docs/stable/advanced.html


arrays = [
	['bar', 'bar', 'baz', 'baz', 'foo', 'foo', 'qux', 'qux'],
	['one', 'two', 'one', 'two', 'one', 'two', 'one', 'two']
]
tuples = list(zip(*arrays))
index = pd.MultiIndex.from_tuples(tuples, names=['first', 'second'])
df = pd.DataFrame(np.random.randn(8, 4), index=arrays)

# index can be tuples
pd.Series(np.random.randn(8), index=tuples)

# control sparse printing of indexes
pd.set_option('display.multi_sparse', False)
df
pd.set_option('display.multi_sparse', True)

# pull level labels
index
index.get_level_values(0) # pull first level of multiindex
index.get_level_values('second') # pull second level of multiindex

# select data by partial label (using index / mi)
df = pd.DataFrame(np.random.randn(3, 8), index=['A', 'B', 'C'], columns=index)
df['bar'] # select by partial label
df['bar', 'one'] # NO CHAINING here; not df['bar']['one']
df['one', 'bar'] # doesn't work other way around

# Even if you slice an index, pandas will print out ALL index levels
df.columns # prints all
df[['foo', 'qux']].columns # slices, then still prints all (for performance reasons)
df[['foo', 'qux']].columns.values # if you to see levels used
df[['foo', 'qux']].columns.get_level_values(0) # for levels used
df[['foo', 'qux']].columns.get_level_values(1) # for levels used


s = pd.Series(np.random.randn(8), index=arrays)
s + s[:-2]
s + s[::2] # adding s to missing values / nans will produce nans


s.reindex(index[:3]) # use another multiindex using reindex


# Advanced indexing with hierarchical index
df = df.T
df.loc['bar']
df.loc['bar', 'two'] # one label supplied per multiindex label
df.loc['baz':'foo']
df.loc['baz':'qux'] # a la base::subset(<df>, select = 'Column.A':'Column.B')
# slice with range of values using tuples
df.loc[('baz', 'two'):('qux', 'one')] # (<level 0>, <level 1>):(<level 0>, <level 1>)
df.loc[('baz', 'two'):'foo']
# passing list of labels or tuples is like reindexing:
df.ix[[('bar', 'two'), ('qux', 'one')]]
# So it's either a range of tuples or a list of tuples for subsetting by
# 	multiindex


# using slicers
def mklbl(prefix,n):
	return ["%s%s" % (prefix,i)  for i in range(n)]

miindex = pd.MultiIndex.from_product([
	mklbl('A',4),
	mklbl('B',2),
	mklbl('C',4),
	mklbl('D',2)
])

micolumns = pd.MultiIndex.from_tuples(
	[
		('a','foo'),
		('a','bar'),
		('b','foo'),
		('b','bah')
	],
	names = ['lvl0', 'lvl1']
)

dfmi = pd.DataFrame(
		np.arange(len(miindex)*len(micolumns)).reshape((len(miindex),len(micolumns))),
		index=miindex,
  	columns=micolumns
	).sort_index().sort_index(axis=1)

dfmi

dfmi.loc[(slice('A1', 'A3'), slice(None), ['C1', 'C3']), :]
# Subsetting via multiindex:
# 	Rows:
# 		level 0: A1 thru A3
# 		level 1: None / select all
# 		level 2: C1 and C3 only
# 		level 3: None / select all
# 	Columns:
#			all
idx = pd.IndexSlice
dfmi.loc[idx[:, :, ['C1', 'C3']], idx[:, 'foo']] # syntax shortcut for above
dfmi.loc[pd.IndexSlice[:, :, ['C1', 'C3']], pd.IndexSlice[:, 'foo']] # same
# 	as above. You can just use : instead of slice(None), and throw in a list
# 	instead of writing out 'slice'

# complicated selections
dfmi.loc['A1', (slice(None), 'foo')] # row where label is A1, column where
# 	second level of index is 'foo'
dfmi.loc[pd.IndexSlice[:, :, ['C1', 'C3']], pd.IndexSlice[:, 'foo']] # rows
# 	where row ix level 3 is c1 and c3; col where col ix level 2 is foo.
# 	completely label-based selection.

# boolean indexer
mask = dfmi[('a', 'foo')] > 200 # kinda like
# 	mtcars[mtcars$mpg > 200 & mtcars$cyl > 200, ]
# 	dfmi columns label 1 is a, columns label 2 is foo, and values in that
# 	column are > 200
dfmi.loc[idx[mask, :, ['C1', 'C3']], idx[:, 'foo']] # same as previous, but
# 	USE BOOLEAN SERIES ALONG WITH pd.IndexSlice IN ADDITION TO INDEX LABEL
# 	SELECTIONS.
dfmi.loc(axis = 0)[:, :, ['C1', 'C3']] # TO USE axis TO PASS THE SLICERS TO
# 	A CERTIAIN AXIS: ROWS OR COLS
dfmi.loc(axis = 1)[:, 'foo']

# set values using axis to pass slicers
df2 = dfmi.copy()
df2.loc(axis = 0)[:, :, ['C1', 'C3']] = -10
df2.loc(axis = 1)[:, 'foo'] = 999
df2 = dfmi.copy()
df2.loc[idx[:, :, ['C1', 'C3']], :] = df2 * 1000 # use right hand side in
# 	setting values as well

# cross-section
df.xs('one', level = 'second')
df.xs('baz', level = 'first') # alternate label subsetting
df.loc[(slice(None), 'one'), :]
df = df.T
df.xs('one', level = 'second', axis = 1)
df.loc[:, ('bar', 'one')]
# don't see why this matters; probably fine to just use other ways of label
# 	subsetting
df.xs('one', level = 'second', axis = 1, drop_level = False) # don't throw 
# 	out the level that you're selecting
df.xs('one', level = 'second', axis = 1, drop_level = True)

# Advanced reindexing and alignment
midx = pd.MultiIndex(
	levels=[['zero', 'one'], ['x','y']],
	labels=[[1,1,0,0],[1,0,1,0]]
)
df = pd.DataFrame(np.random.randn(4,2), index=midx)
df2 = df.mean(level = 0) # THIS IS CRAZY - it's like multiindex makes every
#	 object already a groupby object, so groupwise and split apply combine are
# 	like a step away.
df.sum(level = 0)
df.sum(level = 1)
df.sum(level = 1, axis = 0)
df.sum(level = 0, axis = 1) # bad example, but all groupwise stats accross
# 	columns instead of rows just by using axis = 1
df2.reindex(df.index, level = 0) # expands / grows object by using index
# 	that has more categories than there are rows in the df
df_aligned, df2_aligned = df.align(df2, level = 0)

# multiindexes are intended to be sorted
import random; random.shuffle(tuples)
s = pd.Series(np.random.randn(8), index=pd.MultiIndex.from_tuples(tuples))
# s ix not sorted
s.sort_index(level=0) # sorts on the first level
s.sort_index(level = 1) # sort on the second level
# pass level name instead
s.index.set_names(['L1', 'L2'], inplace = True)
s.sort_index(level = 'L1')
s.sort_index(level = 'L2')
# working with indexes that aren't sorted is bad, but works ok sometimes. avoid
s['qux']
s.sort_index(level = 1)['qux']
# higher dim objects, sort by axis by multiindex
df.T.sort_index(level = 1, axis = 1) # sort by cols, using level 2 on cols

# MultiIndex object checks sort depth
tuples = [('a', 'a'), ('a', 'b'), ('b', 'a'), ('b', 'b')]
idx = pd.MultiIndex.from_tuples(tuples)
idx.lexsort_depth # HERE, WE KNOW THAT THE MULTIINDEX IS SORTED BY TWO
# 	LEVELS: LEVEL 1 AND LEVEL 2
reordered = idx[[1, 0, 3, 2]] # So I think what's happening here is that
# 	you're ordering by level 1 only. level 2 may or may not be sorted; we
# 	don't know. We only know what the index is sorted by level one.
reordered.lexsort_depth # HERE, EVEN THOUGH THERE ARE TWO LEVELS, IT'S ONLY
# 	SORTED BY THE FIRST LEVEL.
s = pd.Series(np.random.randn(4), index=reordered)
s2 = pd.Series(np.random.randn(4), index=idx)
s.ix['a':'a']
# but
s.ix[('a', 'b'):('b', 'a')] # so you can't subset if you've only sorted
# 	accross one level of the multiindex
s3 = s.sort_index()
s3.ix['a':'a']
s3.ix[('a', 'b'):('b', 'a')] # this works becuase lex sort level is same as 
# 	number of levels in index





=== STOPPED HERE AT TAKE METHODS ==================
	Similar to numpy ndarrays, pandas Index, Series, and DataFrame 
