import pandas as pd
import glob

filenames = glob.glob("data/*.csv")

articles = []
col_names = ['title', 'abstract', 'author', 'source', 'time_stamp', 'link']

for filename in filenames:
    articles.append(pd.read_csv(filename, names=col_names))

# Concatenate all data into one DataFrame
big_frame = pd.concat(articles, ignore_index=True)

# times = big_frame['temp_time_stamp'].tolist()
# new_times = list()

# #convert time to proper format
# for t in times:
#     t = t[:10]
#     new_times.append(t)
#     print(new_times)
#
# big_frame.insert(loc=4, column='time_stamp', value=new_times)

big_frame.drop_duplicates(inplace=True) # removes any duplicate rows

del big_frame['source']
del big_frame['link']
# del big_frame['temp_time_stamp']

# assign article id
shape = big_frame.shape
num_rows = shape[0]
key_vals = []

# get number of rows
for x in range(num_rows):
    key_vals.append(x)

# insert article id 0-n
big_frame.insert(loc=0, column='article_id', value=key_vals)
print(big_frame)

print(big_frame.values)
data_types = big_frame.dtypes
print(data_types)

# create cleaned csv file for future use
new_frame = big_frame.to_csv('cleaned_data', index=False)

Article = big_frame[['article_id', 'title', 'abstract']]
Abstract = big_frame[['article_id', 'abstract']]
Author = big_frame[['author', 'title', 'time_stamp']]

Article.to_csv('Article', index=False)
Abstract.to_csv('Abstract', index=False)
Author.to_csv('Author', index=False)