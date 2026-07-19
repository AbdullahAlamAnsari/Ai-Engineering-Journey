import pandas as pd
import numpy as np

# SECTION 1
# Question 1

df = pd.read_csv("fifa_world_cup_squads - fifa_world_cup_squads.csv")
print(df.head(10))
print(df.info())
print(df.describe())
print(df.shape)
print(df.dtypes)

int_col = df.select_dtypes(include="number")
print(int_col)
text_col = df.select_dtypes(include="object")
print(text_col)

# Describe gives us the rough idea about the dataset we are working with using mean, std and also the 4 quartiles
# it means that mistakenly it has either values like -, ?, or Unknown in it
# It is important to check the data type because we will know what operations we can apply on it


# Question 2

wc2022 = df.loc[df['World_Cup_Year'] == 2022]
print(wc2022[['Player Name', 'Country ', 'Age']].head(10))

regular_players = df.loc[df['Matches_Played'] >= 6]
print(f"Total regular players record: {len(regular_players)}")


# Question 3

senior_players = df.loc[df['Age'] > 30]
print(f"Total senior players record: {len(senior_players)}")

worldcup22_5match = df.loc[(df['World_Cup_Year'] == 2022) & (df['Matches_Played'] > 5)]
print(f"Total players record in world cup 2022 with more than 5 matches: {len(worldcup22_5match)}")

print(f"Total players with 3 or more assists: {len(df.loc[df['Assists'] >= 3])}")

# loc works with names and labels / iloc works with indexes
# boolean masking helps in filtering the data


# SECTION 2
# Question 4

print(f"Missing values in each column:\n{df.isnull().sum()}")

col = df.columns

# --- Goals cleanup ---
print(df["Goals"].value_counts())

df['Goals'] = df['Goals'].replace(['N/A', '?', '-'], np.nan)
df['Goals'] = pd.to_numeric(df['Goals'], errors='coerce')  # convert to numeric so comparisons work

print("Missing counts AFTER replacing disguised values with NaN:")
print(df.isnull().sum())
print(df["Goals"].value_counts())

# keep rows where Goals is a valid non-negative number OR still missing
df = df[(df["Goals"] >= 0) | (df["Goals"].isna())]


# --- Market Value cleanup ---
print(df["Market Value"].value_counts())

df['Market Value'] = df['Market Value'].str.replace("€", "").str.replace("M", "")
df['Market Value'] = df['Market Value'].replace(['N/A', '?', '-', 'Unknown'], np.nan)
df['Market Value'] = pd.to_numeric(df['Market Value'], errors='coerce')  # convert to numeric for math

print(df['Market Value'].head())



df['Last Updated'] = pd.to_datetime(df['Last Updated'], errors="coerce")

print(df["Age"].value_counts())
df = df[(df["Age"] >= 0) & (df["Age"] <= 100)]
print(df["Age"].value_counts())
df['Age'] = pd.to_numeric(df['Age'], errors='coerce')

print(df.duplicated(subset = "Player_ID").sum())
print(len(df))
df = df.drop_duplicates(subset = "Player_ID", keep = "first")
print(len(df))

#since duplication will result in double or tripple the stats of each player, we will drop the duplicates and keep the first one. This is because the first one is the most recent one and will have the most updated stats of the player 

#Question - 7 


df.columns = df.columns.str.strip().str.lower().str.replace(" ","_",regex = False)

print(df.head())

df = df.drop(columns = ["club"])
print(df.head())

df = df.set_index("player_id")

#Question - 8 

print(df.describe(include = "all"))
print(df.isnull().sum())
cols = ["age", "world_cup_year", "matches_played", "goals", "assists","minutes_played"]
for col in cols:
    mean = df[col].mean()
    df[col] = df[col].fillna(mean)   # assign back to the column, no inplace

for c in ["market_value"]:
    median = df[c].median()
    df[c] = df[c].fillna(median)

print(df.isnull().sum())

print(df["world_cup_year"].value_counts())
print(df["goals"].sort_values(ascending = False).head(10))



avg_goals_2022 = df.loc[df['world_cup_year'] == 2022, 'goals'].mean()
avg_goals_2018 = df.loc[df['world_cup_year'] == 2018, 'goals'].mean()
print(f"Average goals - 2022 World Cup: {avg_goals_2022:.2f}")
print(f"Average goals - 2018 World Cup: {avg_goals_2018:.2f}")
print(f"Difference (2022 - 2018): {avg_goals_2022 - avg_goals_2018:.2f}") 

avg_mv_over30 = df.loc[df['age'] > 30, 'market_value'].mean()
avg_mv_30under = df.loc[df['age'] <= 30, 'market_value'].mean()
print(f"Average market value - Age > 30: €{avg_mv_over30:.2f}M")
print(f"Average market value - Age <= 30: €{avg_mv_30under:.2f}M")
print(f"Difference (over30 - 30under): €{avg_mv_over30 - avg_mv_30under:.2f}M")

print(df['country'].value_counts().head(20))
print()
print(f"Number of distinct raw spellings/casings in 'country': {df['country'].nunique()}")
