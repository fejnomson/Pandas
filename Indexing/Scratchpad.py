Enter file contents here

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


