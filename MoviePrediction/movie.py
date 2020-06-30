import os
from collections import defaultdict
import sys
import pickle
import pandas as pd

data_folder = os.path.join("ml-100k")
ratings_filename = os.path.join(data_folder, "u.data")

all_ratings = pd.read_csv(ratings_filename, delimiter="\t", header=None,
                          names=["UserID", "MovieID", "Rating", "Datetime"])
all_ratings["Datetime"] = pd.to_datetime(all_ratings['Datetime'], unit='s')

# create new feature (Type: True/False)
all_ratings["Favorable"] = all_ratings["Rating"] > 3

with open("all_ratings.pkl", 'wb') as handle:
    pickle.dump(all_ratings, handle)

# create training dataset (UserID: 1-200)
ratings = all_ratings[all_ratings["UserID"].isin(range(200))]

# create new dataset to only include favorable movies
favorable_ratings = ratings[ratings["Favorable"] == True]
# create new dataset groupby userID to go through each movie watched by a user
favorable_reviews_by_users = dict( (k, frozenset(v.values))  for k, v in favorable_ratings.groupby("UserID")["MovieID"])
#create new dataset on the number of fans of each movie
num_favorable_by_movie = ratings[['MovieID', 'Favorable']].groupby('MovieID').sum()
#sort the favorable movies to see the top 5
top_five = num_favorable_by_movie.sort_values(by = "Favorable", ascending = False)[:5]

dataset_dict = {"favorable_ratings": favorable_ratings, "favorable_reviews_by_users": favorable_reviews_by_users,
                "num_favorable_by_movie": num_favorable_by_movie, "top_five": top_five}
with open("dataset_dict.pkl", 'wb') as handle:
    pickle.dump(dataset_dict, handle)



frequent_itemsets = {}
min_support = 50
# Step1
# create set to contain only the movie itself to check its frequency
# movieID use frozenset
frequent_itemsets[1] = dict((frozenset((movie_id,)), row["Favorable"] )
                            for movie_id, row in num_favorable_by_movie.iterrows()
                            if row["Favorable"]>min_support)
#Step2 3
# takes the newly discovered frequent items, create the supersets, and then test if they ae frequent
def find_frequent_itemsets (favorable_reviews_by_users, k_1_itemsets, min_support):
    counts = defaultdict(int)
    for user, reviews in favorable_reviews_by_users.items():
        for itemset in k_1_itemsets:
            if itemset.issubset(reviews):
                for other_reviewed_movie in reviews - itemset:
                    current_superset = itemset | frozenset((other_reviewed_movie,))
                    counts[current_superset] += 1
    return dict([(itemset, frequency) for itemset, frequency in counts.items() if frequency>min_support])

for k in range(2, 20):
    cur_frequent_itemsets = find_frequent_itemsets(favorable_reviews_by_users, frequent_itemsets[k-1], min_support)
    frequent_itemsets[k] = cur_frequent_itemsets
    if len(cur_frequent_itemsets) == 0:
        print("Did not find any frequent itemsets of length {}".format(k))
        sys.stdout.flush()
        break
    else:
        print("I found {} frequent itemsets of length{}".format(len(cur_frequent_itemsets), k))
        sys.stdout.flush()

del frequent_itemsets[1]

filename = "frequent_itemsets.sav"
pickle.dump(frequent_itemsets, open(filename, 'wb'))


