
== not sure if i should be learning python or github desktop in R or 
 machine learning ==
  == dont need github until hire; can push ML to after mba applications ==

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


