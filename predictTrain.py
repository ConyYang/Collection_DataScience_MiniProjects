import pickle
from collections import defaultdict
from operator import itemgetter
from movieName import get_movie_name

frequent_itemsets = pickle.load(open('frequent_itemsets.sav', 'rb'))

candidate_rules = []
def get_candidate_rules():
    for itemset_length, itemset_counts in frequent_itemsets.items():
        for itemset in itemset_counts.keys():
            for conclusion in itemset:
                premise = itemset - set((conclusion, ))
                candidate_rules.append((premise, conclusion))
    return candidate_rules

candidate_rules = get_candidate_rules()
correct_counts_test = defaultdict(int)
incorrect_counts_test = defaultdict(int)

with open('dataset_dict.pkl', 'rb') as handle:
    dataset_dict = pickle.load(handle)
# dict_keys(['favorable_ratings', 'favorable_reviews_by_users', 'num_favorable_by_movie', 'top_five'])
with open('movieName.pkl', 'rb') as handle:
    movieName = pickle.load(handle)

def count(dataset):
    for user, reviews in dataset.items():
        for candidate_rule in candidate_rules:
            premise, conclusion = candidate_rule
            if premise.issubset(reviews):
                if conclusion in reviews:
                    correct_counts_test[candidate_rule] += 1
                else:
                    incorrect_counts_test[candidate_rule] +=1
    return correct_counts_test, incorrect_counts_test

correct_counts_test, incorrect_counts_test = count(dataset_dict['favorable_reviews_by_users'])

rule_confidence = {candidate_rule:
                       correct_counts_test[candidate_rule] /
                       float(correct_counts_test[candidate_rule] + incorrect_counts_test[candidate_rule])
                        for candidate_rule in candidate_rules}

sorted_confidence = sorted(rule_confidence.items(), key=itemgetter(1), reverse=True)

# for index in range (len(sorted_confidence)):
#     print("Rule #{0}".format(index+1))
#     (premise, conclusion) = sorted_confidence[index][0]
#     premise_movie_names = ", ".join(get_movie_name(idx) for idx in premise)
#     conclusion_movie_name = get_movie_name(conclusion)
#     print("Rule: If a person recommends {0} they will also recommend {1}".format(premise_movie_names, conclusion_movie_name))
#     print("-- Confidence ：{}".format(rule_confidence[(premise, conclusion)]))
#     print(" ")

with open("all_ratings.pkl", 'rb') as handle:
    all_ratings = pickle.load(handle)

test_dataset = all_ratings[~all_ratings['UserID'].isin(range(200))]
test_favorable = test_dataset[test_dataset["Favorable"] == True]
test_favorable_by_users = dict((k, frozenset(v.values)) for k,v in
                               test_favorable.groupby("UserID")["MovieID"])

correct_counts_test, incorrect_counts_test = count(test_favorable_by_users)


test_confidence = {candidate_rule:
                       correct_counts_test[candidate_rule] /
                       float(correct_counts_test[candidate_rule] + incorrect_counts_test[candidate_rule])
                   for candidate_rule in rule_confidence}

for index in range (len(sorted_confidence)):
    print("Rule #{0}".format(index+1))
    (premise, conclusion) = sorted_confidence[index][0]
    premise_movie_names = ", ".join(get_movie_name(idx) for idx in premise)
    conclusion_movie_name = get_movie_name(conclusion)
    print("Rule: If a person recommends {0} they will also recommend {1}".format(premise_movie_names, conclusion_movie_name))
    print("-- Train Confidence ：{}".format(rule_confidence[(premise, conclusion)]))
    print("-- Test Confidence ：{}".format(test_confidence[(premise, conclusion)]))
    print(" ")
