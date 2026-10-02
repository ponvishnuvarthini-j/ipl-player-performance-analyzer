"""
PROJECT 4: IPL Player Performance Analyzer
----------------------------------------------
You have player stats from a T20 league season across 5 teams.
Complete each TODO in order.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------------------------------
# STEP 1 (Day 24): Load data
# -----------------------------------------------------
# TODO: Read 'ipl_players.csv' into df
# TODO: Read 'teams.csv' into teams_df

df = pd.read_csv("ipl_players.csv")
teams_df = pd.read_csv("teams.csv")


# -----------------------------------------------------
# STEP 2 (Day 25): Explore
# -----------------------------------------------------
# TODO: head, tail, info, describe, isnull().sum()

print(df.head())

print(df.tail())

print(df.info())

print(df.describe())

print(df.isnull().sum())


# -----------------------------------------------------
# STEP 3 (Day 26): Clean
# -----------------------------------------------------
# TODO: Drop duplicate rows
# TODO: Fill missing StrikeRate and Economy with 0
#       (a batsman genuinely has no economy, and vice versa -- 0 is a
#        valid placeholder here, NOT the column mean)

df = df.drop_duplicates()

df["StrikeRate"] = df["StrikeRate"].fillna(0)

df["Economy"] = df["Economy"].fillna(0)


# -----------------------------------------------------
# STEP 4 (Day 22 + 21): Function with if-elif
# -----------------------------------------------------
# TODO: Write function classify_role(wickets, runs) that returns:
#       'Bowler' if wickets >= 15, 'Batsman' if runs >= 300,
#       else 'All-rounder'
# TODO: Create a new column 'Role' using this function

def classify_role(wickets, runs):

    if wickets >= 15:
        return "Bowler"

    elif runs >= 300:
        return "Batsman"

    else:
        return "All-rounder"

roles = []

wickets_list = df["Wickets"].tolist()

runs_list = df["Runs"].tolist()

for i in range(len(df)):

    role = classify_role(
        wickets_list[i],
        runs_list[i]
    )

    roles.append(role)

df["Role"] = roles


# -----------------------------------------------------
# STEP 5 (Day 27): Filter, sort, rename
# -----------------------------------------------------
# TODO: Filter all players with Role == 'Bowler'
# TODO: Sort df by 'Runs' descending, print top 5 run scorers
# TODO: Rename column 'StrikeRate' to 'SR'

bowlers = df[df["Role"] == "Bowler"]

print(bowlers)

top_runs = df.sort_values(
    by="Runs",
    ascending=False
)

print(top_runs.head(5))

df.rename(
    columns={"StrikeRate": "SR"},
    inplace=True
)


# -----------------------------------------------------
# STEP 6 (Day 29): Merge
# -----------------------------------------------------
# TODO: Merge df with teams_df on 'Team' column -> merged_df

merged_df = pd.merge(
    df,
    teams_df,
    on="Team"
)


# -----------------------------------------------------
# STEP 7 (Day 28): GroupBy
# -----------------------------------------------------
# TODO: Group merged_df by 'Team' -> total Runs, total Wickets
#       (hint: .agg({'Runs': 'sum', 'Wickets': 'sum'}))
# TODO: Group merged_df by 'Role' -> count of players in each role

team_stats = merged_df.groupby(
    "Team"
).agg({
    "Runs":"sum",
    "Wickets":"sum"
})

print(team_stats)

role_count = merged_df.groupby(
    "Role"
).size()

print(role_count)

# -----------------------------------------------------
# STEP 8 (Day 23): NumPy
# -----------------------------------------------------
# TODO: Convert 'Runs' column to NumPy array
# TODO: Print np.mean(), np.max(), np.percentile(array, 75)

runs_array = merged_df["Runs"].to_numpy()

print(np.mean(runs_array))

print(np.max(runs_array))

print(np.percentile(
    runs_array,
    75
))


# -----------------------------------------------------
# STEP 9 (Day 20 + 21): List + loop + condition
# -----------------------------------------------------
# TODO: Build a list called all_rounders containing names of every
#       player with Role == 'All-rounder'
# TODO: Print the list

all_rounders = []

players = merged_df["Player"].tolist()

roles = merged_df["Role"].tolist()

for i in range(len(merged_df)):

    if roles[i] == "All-rounder":

        all_rounders.append(
            players[i]
        )

print(all_rounders)


# -----------------------------------------------------
# STEP 10 (Day 30): File handling
# -----------------------------------------------------
# TODO: Export merged_df to 'ipl_analysis.csv'

merged_df.to_csv(
    "ipl_analysis.csv",
    index=False
)


# -----------------------------------------------------
# STEP 11 (Day 31): Matplotlib
# -----------------------------------------------------
# TODO: Bar chart -> Top 5 run scorers
# TODO: Bar chart -> Total wickets by team

top5 = df.sort_values(
    by="Runs",
    ascending=False
).head(5)

plt.figure(figsize=(8,5))

plt.bar(
    top5["Player"],
    top5["Runs"]
)

plt.title("Top 5 Run Scorers")

plt.show()

team_wickets = merged_df.groupby(
    "Team"
)["Wickets"].sum()

plt.figure(figsize=(8,5))

plt.bar(
    team_wickets.index,
    team_wickets.values
)

plt.title("Total Wickets by Team")

plt.show()

# -----------------------------------------------------
# STEP 12 (Day 32): Seaborn
# -----------------------------------------------------
# TODO: sns.scatterplot of SR vs Economy, colored by Role
# TODO: sns.countplot of Role

sns.scatterplot(
    data=merged_df,
    x="SR",
    y="Economy",
    hue="Role"
)

plt.show()

sns.countplot(
    data=merged_df,
    x="Role"
)

plt.show()

# -----------------------------------------------------
# STEP 13: Conclusion
# -----------------------------------------------------
# TODO: Print the best batsman, best bowler, and the most "balanced"
#       team (highest combined runs+wickets)

max_runs = 0

best_batsman = ""

players = df["Player"].tolist()

runs = df["Runs"].tolist()

for i in range(len(df)):

    if runs[i] > max_runs:

        max_runs = runs[i]

        best_batsman = players[i]

print(best_batsman)

max_wickets = 0

best_bowler = ""

wickets = df["Wickets"].tolist()

for i in range(len(df)):

    if wickets[i] > max_wickets:

        max_wickets = wickets[i]

        best_bowler = players[i]

print(best_bowler)

team_balance = merged_df.groupby(
    "Team"
).agg({
    "Runs":"sum",
    "Wickets":"sum"
})

team_balance["Total"] = (
    team_balance["Runs"]
    +
    team_balance["Wickets"]
)

best_team = ""

max_total = 0

for team in team_balance.index:

    total = team_balance.loc[
        team,
        "Total"
    ]

    if total > max_total:

        max_total = total

        best_team = team

print(best_team)

# ==================================DONE!!!=============================
