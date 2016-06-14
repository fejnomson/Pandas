

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
<stopped>

# where() method and masking
...stopped here...

