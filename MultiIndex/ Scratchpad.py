
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


x = pd.DataFrame({'x': [1, 2, 3], 'y': [3, 4, 5]})
x
x.iloc[1] = {'x': 999, 'y': 999} # can use dictionary to re-assign rows

s1 = pd.Series(np.random.randn(6),index=list('abcdef'))
# .loc for index-based subsetting
s1.loc['c':]
s1.loc['b']
