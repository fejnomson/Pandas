

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

data_df = <??>
countries = array(['US', 'UK', 'GR', 'JP'])
key = countries[random.randint(0, 4, 1000)]
grouped = data_df.groupby(key)


# FILTRATION
sf = Series([1, 1, 2, 3, 3, 3])
sf.groupby(sf).filter(lambda x: x.sum() > 2) # filters out observations in the series where the sum for the whole gropu is over 2
sf.groupby(sf) # is a clean way of breaking a series up into groups based on unique values

















