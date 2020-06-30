import pickle
from collections import defaultdict
from operator import itemgetter

frequent_itemsets = pickle.load(open('frequent_itemsets.sav', 'rb'))

candidate_rules = []
for itemset_length, itemset_counts in frequent_itemsets.items():
    for itemset in itemset_counts.keys():
        for conclusion in itemset:
            premise = itemset - set((conclusion, ))
            candidate_rules.append((premise, conclusion))

correct_counts = defaultdict(int)
incorrect_counts = defaultdict(int)

with open('dataset_dict.pkl', 'rb') as handle:
    dataset_dict = pickle.load(handle)
# dict_keys(['favorable_ratings', 'favorable_reviews_by_users', 'num_favorable_by_movie', 'top_five'])

for user, reviews in dataset_dict['favorable_reviews_by_users'].items():
    for candidate_rule in candidate_rules:
        premise, conclusion = candidate_rule
        if premise.issubset(reviews):
            if conclusion in reviews:
                correct_counts[candidate_rule] += 1
            else:
                incorrect_counts[candidate_rule] +=1

rule_confidence = {candidate_rule:
                       correct_counts[candidate_rule]/
                       float(correct_counts[candidate_rule]+incorrect_counts[candidate_rule])
                        for candidate_rule in candidate_rules}
sorted_confidence = sorted(rule_confidence.items(), key=itemgetter(1), reverse=True)
for index in range (len(sorted_confidence)):
    print("Rule #[0]".format(index+1))
    (premise, conclusion) = sorted_confidence[index][0]
    print("Rule: If a person recommends {0} they will also recommend {1}".format(premise, conclusion))
    print("-- Confidence ：{}".format(rule_confidence[(premise, conclusion)]))
    print(" ")
