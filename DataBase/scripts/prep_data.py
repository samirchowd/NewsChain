import pandas as pd
import glob

filenames = glob.glob("../data/*.csv")

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

# hash function to generate article id. Uses link, because it is a unique value for each article
key_vals = []
print(big_frame)
for i, row in big_frame.iterrows():
    key = hash(row['link'])
    if key not in key_vals:
        key_vals.append(key)
    else:
        key = hash(row['title'])
        if key not in key_vals:
            key_vals.append(key)
big_frame.insert(loc=0, column='article_id', value=key_vals)
print(len(big_frame))

# create cleaned csv file for future use
big_frame.to_csv('../data/cleaned_data', index=False)