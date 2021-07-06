# run -> python trend_analysis1.py --dataset datasets/USvideos.csv --json_file datasets/US_category_id.json

##################################################################################################################################

import pandas as pd
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
import seaborn as sns
import argparse
import warnings
from collections import Counter
import datetime
import wordcloud
import json

from IPython.display import set_matplotlib_formats



ap = argparse.ArgumentParser()
ap.add_argument("-ds", "--dataset", required=True)
ap.add_argument("-js", "--json_file", required=True)

args = vars(ap.parse_args())

##################################################################################################################################

# Configuring some options
'exec(%matplotlib inline)'

# If you want interactive plots, uncomment the next line
'exec(%matplotlib notebook)'

set_matplotlib_formats('retina')


##################################################################################################################################

# Hiding warnings for cleaner display
warnings.filterwarnings('ignore')

##################################################################################################################################

#Reading the dataset
dataset_path = args["dataset"]
df = pd.read_csv(dataset_path)


##################################################################################################################################

pd.options.display.float_format = '{:.2f}'.format

##################################################################################################################################

#Info. of the dataset
print('\n\n\n')
print('#################################### Overview of the data #################################### \n')
print(df.head(10))

print('\n\n')
print(df.info())

##################################################################################################################################

#Data cleaning
df[df["description"].apply(lambda x: pd.isna(x))].head(3)


df["description"] = df["description"].fillna(value="")

##################################################################################################################################

#Dataset collection years
cdf = df["trending_date"].apply(lambda x: '20' + x[:2]).value_counts() \
            .to_frame().reset_index() \
            .rename(columns={"index": "year", "trending_date": "No_of_videos"})

fig, ax = plt.subplots()
_ = sns.barplot(x="year", y="No_of_videos", data=cdf, ax=ax)
_ = ax.set(xlabel="Year", ylabel="No. of videos")
plt.show()


df["trending_date"].apply(lambda x: '20' + x[:2]).value_counts(normalize=True)

##################################################################################################################################

#Statistical description of numerical columns
print('\n\n\n')
print('#################################### Statistical description of numerical columns #################################### \n')
print(df.describe())

##################################################################################################################################

#Views
fig, ax = plt.subplots()
_ = sns.distplot(df["views"], kde=False, 
                 hist_kws={'alpha': 1}, bins=np.linspace(0, 2.3e8, 47), ax=ax)
_ = ax.set(xlabel="Views", ylabel="No. of videos", xticks=np.arange(0, 2.4e8, 1e7))
_ = ax.set_xlim(right=2.5e8)
_ = plt.xticks(rotation=90)
plt.show()


fig, ax = plt.subplots()
_ = sns.distplot(df[df["views"] < 25e6]["views"], kde=False, hist_kws={'alpha': 1}, ax=ax)
_ = ax.set(xlabel="Views", ylabel="No. of videos")
plt.show()


print('\n\n\n')
print('Number of videos with views( < 1 Million) : ' + str(df[df['views'] < 1e6]['views'].count() / df['views'].count() * 100) + '%')

##################################################################################################################################

#Likes
plt.rc('figure.subplot', wspace=0.9)
fig, ax = plt.subplots()
_ = sns.distplot(df["likes"], kde=False, hist_kws={'alpha': 1}, 
                 bins=np.linspace(0, 6e6, 61), ax=ax)
_ = ax.set(xlabel="Likes", ylabel="No. of videos")
_ = plt.xticks(rotation=90)
plt.show()


fig, ax = plt.subplots()
_ = sns.distplot(df[df["likes"] <= 1e5]["likes"], kde=False, hist_kws={'alpha': 1}, ax=ax)
_ = ax.set(xlabel="Likes", ylabel="No. of videos")
plt.show()


print('\n\n\n')
print()
print('Number of videos with likes( < 40000) : ' + str(df[df['likes'] < 4e4]['likes'].count() / df['likes'].count() * 100) + '%')

##################################################################################################################################

#Comment count
fig, ax = plt.subplots()
_ = sns.distplot(df["comment_count"], kde=False, rug=False, hist_kws={'alpha': 1}, ax=ax)
_ = ax.set(xlabel="Comment Count", ylabel="No. of videos")
plt.show()


fig, ax = plt.subplots()
_ = sns.distplot(df[df["comment_count"] < 200000]["comment_count"], kde=False, rug=False, hist_kws={'alpha': 1}, 
                 bins=np.linspace(0, 2e5, 49), ax=ax)
_ = ax.set(xlabel="Comment Count", ylabel="No. of videos")
plt.show()


print('\n\n\n')
print('Number of videos with comment counts( < 4000) : ' + str(df[df['comment_count'] < 4000]['comment_count'].count() / df['comment_count'].count() * 100) + '%')

##################################################################################################################################

#Description on non-numerical columns
print('\n\n\n')
print('#################################### Description of non-numerical columns #################################### \n')
print(df.describe(include = ['O']))

print('\n\n\n')
print('############################ Trending video appeared more than once on the trending list but with different titles ############################\n')
grouped = df.groupby("video_id")
groups = []
wanted_groups = []
for key, item in grouped:
    groups.append(grouped.get_group(key))

for g in groups:
    if len(g['title'].unique()) != 1:
        wanted_groups.append(g)

print(wanted_groups[0])

##################################################################################################################################

#Trending video titles contain capitalized word.
def contains_capitalized_word(s):
    for w in s.split():
        if w.isupper():
            return True
    return False


df["contains_capitalized"] = df["title"].apply(contains_capitalized_word)

value_counts = df["contains_capitalized"].value_counts().to_dict()

fig, ax = plt.subplots()
_ = ax.pie([value_counts[False], value_counts[True]], labels=['No', 'Yes'], startangle=90)
_ = ax.axis('equal')
_ = ax.set_title('Title Contains Capitalized Word?')
plt.show()


print('\n\n\n')
print('Trending video titles contain capitalized word : ' + str(len(df[(df["contains_capitalized"] == True) & (df["contains_capitalized"] == True)].index)))

##################################################################################################################################

#Video title lengths
df["title_length"] = df["title"].apply(lambda x: len(x))

fig, ax = plt.subplots()
_ = sns.distplot(df["title_length"], kde=False, rug=False, hist_kws={'alpha': 1}, ax=ax)
_ = ax.set(xlabel="Title Length", ylabel="No. of videos", xticks=range(0, 110, 10))
plt.show()


fig, ax = plt.subplots()
_ = ax.scatter(x=df['views'], y=df['title_length'], edgecolors="#000000", linewidths=0.5)
_ = ax.set(xlabel="Views", ylabel="Title Length")
plt.show()


##################################################################################################################################

#Correlation between dataset variables
h_labels = [x.replace('_', ' ').title() for x in 
            list(df.select_dtypes(include=['number', 'bool']).columns.values)]

fig, ax = plt.subplots(figsize=(10,6))
_ = sns.heatmap(df.corr(), annot=True, xticklabels=h_labels, yticklabels=h_labels, cmap=sns.cubehelix_palette(as_cmap=True), ax=ax)
plt.show()

#Views and likes
fig, ax = plt.subplots()
_ = plt.scatter(x=df['views'], y=df['likes'], linewidths=0.5)
_ = ax.set(xlabel="Views", ylabel="Likes")
plt.show()


##################################################################################################################################

#Most common words in video titles
title_words = list(df["title"].apply(lambda x: x.split()))
title_words = [x for y in title_words for x in y]
print('\n\n\n#################################### Most common words in video titles #################################### \n')
print(Counter(title_words).most_common(25))

##################################################################################################################################

wc = wordcloud.WordCloud(width=1000, height=400, collocations=False).generate(" ".join(title_words))
plt.figure(figsize=(15,10))
plt.imshow(wc, interpolation='bilinear')
_ = plt.axis("off")
plt.show()

##################################################################################################################################

#Channels withlargest number of trending videos.
cdf = df.groupby("channel_title").size().reset_index(name="video_count") \
    .sort_values("video_count", ascending=False).head(20)

fig, ax = plt.subplots(figsize=(8,8))
_ = sns.barplot(x="video_count", y="channel_title", data=cdf, ax=ax)
_ = ax.set(xlabel="No. of videos", ylabel="Channel")
plt.show()

##################################################################################################################################

#Video categories with largest number of trending videos
with open(args["json_file"]) as f:
    categories = json.load(f)["items"]
cat_dict = {}
for cat in categories:
    cat_dict[int(cat["id"])] = cat["snippet"]["title"]
df['category_name'] = df['category_id'].map(cat_dict)

cdf = df["category_name"].value_counts().to_frame().reset_index()
cdf.rename(columns={"index": "category_name", "category_name": "No_of_videos"}, inplace=True)
fig, ax = plt.subplots()
_ = sns.barplot(x="category_name", y="No_of_videos", data=cdf, ax=ax)
_ = ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
_ = ax.set(xlabel="Category", ylabel="No. of videos")
plt.show()

##################################################################################################################################

#Video publishing time
df["publishing_day"] = df["publish_time"].apply(
    lambda x: datetime.datetime.strptime(x[:10], "%Y-%m-%d").date().strftime('%a'))
df["publishing_hour"] = df["publish_time"].apply(lambda x: x[11:13])
df.drop(labels='publish_time', axis=1, inplace=True)


cdf = df["publishing_day"].value_counts()\
        .to_frame().reset_index().rename(columns={"index": "publishing_day", "publishing_day": "No_of_videos"})
fig, ax = plt.subplots()
_ = sns.barplot(x="publishing_day", y="No_of_videos", data=cdf, ax=ax)
_ = ax.set(xlabel="Publishing Day", ylabel="No. of videos")
plt.show()


cdf = df["publishing_hour"].value_counts().to_frame().reset_index()\
        .rename(columns={"index": "publishing_hour", "publishing_hour": "No_of_videos"})
fig, ax = plt.subplots()
_ = sns.barplot(x="publishing_hour", y="No_of_videos", data=cdf, ax=ax)
_ = ax.set(xlabel="Publishing Hour", ylabel="No. of videos")
plt.show()

##################################################################################################################################

#Videos with an error
value_counts = df["video_error_or_removed"].value_counts().to_dict()
fig, ax = plt.subplots()
_ = ax.pie([value_counts[False], value_counts[True]], labels=['No', 'Yes'])
_ = ax.axis('equal')
_ = ax.set_title('Video Error or Removed?')
plt.show()

print('\n\n\n')
print('Numbers of videos with errors/removed : ' + str(len(df[(df["video_error_or_removed"] == True) & (df["video_error_or_removed"] == True)].index)))

##################################################################################################################################

#Videos with commets disabled
value_counts = df["comments_disabled"].value_counts().to_dict()
fig, ax = plt.subplots()
_ = ax.pie(x=[value_counts[False], value_counts[True]], labels=['No', 'Yes'])
_ = ax.axis('equal')
_ = ax.set_title('Comments Disabled?')
plt.show()

print('\n\n\n')
print('Numbers of videos with comments disabled : ' + str(len(df[(df["comments_disabled"] == True) & (df["comments_disabled"] == True)].index)))


####################################################################################################################################################################################################################################################################

#Videos with ratings disabled
value_counts = df["ratings_disabled"].value_counts().to_dict()
fig, ax = plt.subplots()
_ = ax.pie([value_counts[False], value_counts[True]], labels=['No', 'Yes'])
_ = ax.axis('equal')
_ = ax.set_title('Ratings Disabled?')
plt.show()

print('\n\n\n')
print('Numbers of videos with ratings disabled : ' + str(len(df[(df["ratings_disabled"] == True) & (df["ratings_disabled"] == True)].index)))

##################################################################################################################################

#Videos with comments and ratings(both) disabled
print('\n\n\n')
print('Numbers of videos with comments and ratings(both) disabled : ' + str(len(df[(df["comments_disabled"] == True) & (df["ratings_disabled"] == True)].index)))
print('\n\n\n')

##################################################################################################################################
