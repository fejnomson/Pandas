
http://pandas.pydata.org/pandas-docs/stable/merging.html


# concat does heavy lifting alon an axis
# 	optional set logic of indexes
df1 = pd.DataFrame(
	{
		'A': ['A0', 'A1', 'A2', 'A3'],
		'B': ['B0', 'B1', 'B2', 'B3'],
		'C': ['C0', 'C1', 'C2', 'C3'],
		'D': ['D0', 'D1', 'D2', 'D3']
	},
	index = [0, 1, 2, 3]
)
df2 = pd.DataFrame(
	{
		'A': ['A4', 'A5', 'A6', 'A7'],
		'B': ['B4', 'B5', 'B6', 'B7'],
		'C': ['C4', 'C5', 'C6', 'C7'],
		'D': ['D4', 'D5', 'D6', 'D7']
	},
	index = [4, 5, 6, 7]
)
df3 = pd.DataFrame(
	{
		'A': ['A8', 'A9', 'A10', 'A11'],
		'B': ['B8', 'B9', 'B10', 'B11'],
		'C': ['C8', 'C9', 'C10', 'C11'],
		'D': ['D8', 'D9', 'D10', 'D11']
	},
	index = [8, 9, 10, 11]
)
frames = [df1, df2, df3]
result = pd.concat(frames) # plyr::rbind.fill()
# can apply to series, dataframes, or panel objects
# specify axis (instead of calling rbind or cbind, just one function with an arg)
result = pd.concat(frames, keys = ['x', 'y', 'z']) # i really like this
# 	because it's kinda like frames[0].loc[:, 'data source'] = 'x', etc. - 
# 	saves the step of assigning all those fields yourself.
result.ix['y'] # then subset by input df
result = pd.concat(frames, keys = ['x', 'y', 'z'], ignore_index = True) # Make new index
frames = [df3, df2, df1]
result = pd.concat(frames, ignore_index = True)
result = pd.concat(frames, keys = ['x', 'y', 'z'])
# not completely sure how to handle indexes, but
result.reset_index(level = 0, drop = True) # Looks like this works?
x.loc['y', :]

