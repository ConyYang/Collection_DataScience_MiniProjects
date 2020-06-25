import pandas as pd
from collections import defaultdict

dataset = pd.read_csv('data.csv')
dataset.columns = ["Date", "Start", "Visitorteam", "VisitorPTS", "HomeTeam", "HomePTS", "Score Type", "OT?", "ATTEND", "NOTES"]

# Extract who wins: 1: MainTeam Wins; 0: Visitor Team Wins
dataset["HomeWin"] = dataset["VisitorPTS"] < dataset["HomePTS"]
result_true = dataset["HomeWin"].values

won_last = defaultdict(int)
new_dataset = pd.DataFrame()
for index, row in dataset.sort_values(by="Date").iterrows():
    home_team = row["HomeTeam"]
    visitor_team = row["Visitorteam"]
    row["HomeLastWin"] = won_last[home_team]
    row["VisitorLastWin"] = won_last[visitor_team]
    won_last[home_team] = row["HomeWin"]
    won_last[visitor_team] = not row["HomeWin"]

    print(row)
    dataset.iloc[index] = row


print(dataset)