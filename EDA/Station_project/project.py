import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json

# ============================================================
# LOAD DATA
# ============================================================

scooter = pd.read_csv("scooter.csv")
subway = pd.read_csv("subway.csv")

print(f"Scooter data: \n {scooter.head()}")
print(f"Subway data: \n{subway.head()}")

print(f"Scooter data info: \n {scooter.info()}")
print(f"Subway data info: \n {subway.info()}")

print(f"Scooter data stats: \n {scooter.describe()}")
print(f"Subway data stats: \n {subway.describe()}")

print(f"Subway Data shape: \n {subway.shape}")
print(f"Scooter Data shape: \n {scooter.shape}")

# ============================================================
# PHASE 1: DATA CLEANING
# ============================================================
print("========================== DATA CLEANING ==========================")
print(f"Null values across the data: \n {subway.isnull().sum()}")

# ---- 1.1 station_id standardization ----
print(f"Values before the standardization: {subway['station_id'].nunique()}")
subway["station_id"] = subway["station_id"].str.lower().str.strip()
print(f"Values after the standardization: {subway['station_id'].nunique()}")  # exactly 10 values

# ---- 1.1 start_lat / start_lng cleaning ----
# FIX: removed the "\-" from the regex character class below.
# The old regex [N\-°W%n] was stripping the MINUS SIGN out of every
# longitude value, turning all negative longitudes (-74.00...) into
# positive ones (74.00...). That silently broke every later filter
# that relied on real negative longitudes (like the STN_003 bounding box).
scooter["start_lat"] = (
    scooter["start_lat"]
    .str.lower()
    .str.strip()
    .str.replace(r"[n°w%]", "", regex=True)
)
print(scooter["start_lat"].unique())

scooter["start_lng"] = (
    scooter["start_lng"]
    .str.lower()
    .str.strip()
    .str.replace(r"[n°w%]", "", regex=True)
)
print(scooter["start_lng"].unique())

scooter["start_lng"] = pd.to_numeric(scooter["start_lng"], errors="coerce")
scooter["start_lat"] = pd.to_numeric(scooter["start_lat"], errors="coerce")

print(scooter.dtypes)
print("start_lng range after fix:", scooter["start_lng"].min(), "to", scooter["start_lng"].max())
# All values converted to float, and start_lng should now show NEGATIVE numbers

# ---- 1.2 battery_level cleaning ----
print(scooter["battery_level"].value_counts())

scooter["battery_level"] = (
    scooter["battery_level"]
    .str.strip()
    .str.replace(r"[N\-°W%n]", "", regex=True)
)
print(scooter["battery_level"].value_counts())
print(scooter["battery_level"].isna().sum().sum())

scooter["battery_level"] = pd.to_numeric(scooter["battery_level"], errors="coerce")

print(f"Nan values before dropping: {scooter['battery_level'].isna().sum().sum()}")
scooter = scooter.dropna(subset=["battery_level"])
print(f"Nan values after dropping: {scooter['battery_level'].isna().sum().sum()}")

# ---- 1.2 entries / exits cleaning ----
print(subway.head())

print(f"Nan values before conversion: {subway['entries'].isna().sum().sum()}")
subway["entries"] = pd.to_numeric(subway["entries"], errors="coerce")
print(f"Nan values before dropping: {subway['entries'].isna().sum().sum()}")
subway = subway.dropna(subset=["entries"])
print(f"Nan values after dropping: {subway['entries'].isna().sum().sum()}")

print(f"Nan values before conversion: {subway['exits'].isna().sum().sum()}")
subway["exits"] = pd.to_numeric(subway["exits"], errors="coerce")
print(f"Nan values before dropping: {subway['exits'].isna().sum().sum()}")
subway = subway.dropna(subset=["exits"])
print(f"Nan values after dropping: {subway['exits'].isna().sum().sum()}")

# ---- 1.2 user_rating cleaning ----
print(scooter["user_rating"].value_counts())
print(scooter["user_rating"].head(15))

scooter["user_rating"] = pd.to_numeric(scooter["user_rating"], errors="coerce")
mean_rating = scooter["user_rating"].mean().round(0)
print(mean_rating)
scooter["user_rating"] = scooter["user_rating"].fillna(mean_rating)
print(scooter["user_rating"].isna().sum())
print(scooter["user_rating"].value_counts())

print(scooter.dtypes)

# ---- 1.2 start_time / end_time parsing ----
def parse_mixed_datetime(value):
    """
    Takes a single value from start_time/end_time and figures out
    which format it's in, then converts it to a proper datetime.
    """
    value = str(value).strip()

    # Step 1: purely numeric -> Unix epoch timestamp (seconds)
    if value.isdigit():
        return pd.to_datetime(value, unit="s", errors="coerce")

    # Step 2: ISO format (e.g. "2026-06-21 4:03:12")
    parsed = pd.to_datetime(value, format="%Y-%m-%d %H:%M:%S", errors="coerce")
    if pd.notna(parsed):
        return parsed

    # Step 3: US-style format (e.g. "06/08/2026 7:04 PM")
    parsed = pd.to_datetime(value, format="%m/%d/%Y %I:%M %p", errors="coerce")
    if pd.notna(parsed):
        return parsed

    # Step 4: nothing worked
    return pd.NaT


scooter["start_time"] = scooter["start_time"].apply(parse_mixed_datetime)
scooter["end_time"] = scooter["end_time"].apply(parse_mixed_datetime)

print(scooter[["start_time", "end_time"]].head(20))
print(scooter.dtypes)
print("Unparsed start_time rows:", scooter["start_time"].isna().sum())
print("Unparsed end_time rows:", scooter["end_time"].isna().sum())

scooter = scooter.dropna(subset=["start_time", "end_time"])

print("Unparsed start_time rows after dropping:", scooter["start_time"].isna().sum())
print("Unparsed end_time rows after dropping:", scooter["end_time"].isna().sum())

# ---- 1.3 negative entries/exits investigation ----
print(subway["entries"].dtypes)

subway["entries"] = pd.to_numeric(subway["entries"], errors="coerce")
subway["exits"] = pd.to_numeric(subway["exits"], errors="coerce")

neg_entries_pct = (subway["entries"] < 0).mean() * 100
neg_exits_pct = (subway["exits"] < 0).mean() * 100

print(f"Negative entries: {neg_entries_pct:.2f}% of rows")
print(f"Negative exits: {neg_exits_pct:.2f}% of rows")
print(subway["entries"].value_counts())

neg_by_station = subway[subway["entries"] < 0]["station_id"].value_counts()
print("Negative entries by station:")
print(neg_by_station)

subway["timestamp"] = pd.to_datetime(subway["timestamp"], errors="coerce")
subway["hour"] = subway["timestamp"].dt.hour

neg_by_hour = subway[subway["entries"] < 0]["hour"].value_counts().sort_index()
print("Negative entries by hour:")
print(neg_by_hour)

subway["date"] = subway["timestamp"].dt.date
neg_by_day = subway[subway["entries"] < 0]["date"].value_counts()
print("Negative entries by day:")
print(neg_by_day)

col = subway["entries"]
print(f"Max and min values: MAX = {subway['entries'].max()}   MIN = {subway['entries'].min()}")
Q1 = col.quantile(0.25)
Q3 = col.quantile(0.75)
IQR = Q3 - Q1
lower_fence = Q1 - 1.5 * IQR
upper_fence = Q3 + 1.5 * IQR
print("Lower Fence:", lower_fence)
print("Upper Fence:", upper_fence)

outliers_iqr = subway[(col < 0) | (col > upper_fence)]
print("Number of outliers:", len(outliers_iqr))

# Majority of both positive and negative values fall in a realistic range,
# so we treat the negative sign as a sign-flip bug and take the absolute value.
subway["entries"] = abs(subway["entries"])

print(f"Max and min values: MAX = {subway['entries'].max()}   MIN = {subway['entries'].min()}")
print(subway.head())

# ============================================================
# PHASE 2: AGGREGATION & GROUP BY
# ============================================================

total_ent_ex_sta = subway.groupby(["station_id"])[["entries", "exits"]].agg(sum)
print(total_ent_ex_sta)

mean_hour = subway.groupby(["station_id"])[["hour"]].mean()
print(mean_hour)

print(scooter.head())
print(scooter.dtypes)
print(subway.head())

# ---- Daily ride counts + average battery level, city-wide ----
scooter["date"] = scooter["start_time"].dt.date
print(scooter["date"])

daily_ride_counts = scooter.groupby("date").agg(
    ride_count=("ride_id", "count"),
    avg_battery_level=("battery_level", "mean"),
).reset_index()

print(daily_ride_counts)

# ============================================================
# PHASE 3: DAY 15 PIVOT TABLE + HEATMAP
# ============================================================

# Day 15 = 2026-06-15 (per city_heartbeat.json day_number mapping)
day15 = subway[subway["date"] == pd.to_datetime("2026-06-15").date()]

print(f"Day 15 rows: {len(day15)}")
print(f"Stations present on Day 15: {day15['station_id'].nunique()}")

day15_pivot = day15.pivot_table(
    index="hour",
    columns="station_id",
    values="entries",
    aggfunc="sum",
)

print(day15_pivot)

fig, ax = plt.subplots(figsize=(12, 7))

sns.heatmap(
    day15_pivot,
    annot=True,
    fmt=".0f",
    cmap="YlOrRd",
    linewidths=0.5,
    linecolor="white",
    cbar_kws={"label": "Entries"},
    ax=ax,
)

ax.set_xlabel("Station ID")
ax.set_ylabel("Hour of Day")
ax.set_title("Day 15 — Hourly Subway Entries by Station")
plt.xticks(rotation=45, ha="right")

# Highlight the disputed 14:00-20:00 window
hours = list(day15_pivot.index)
if 14 in hours and 20 in hours:
    y_start = hours.index(14)
    y_end = hours.index(20) + 1
    ax.axhspan(y_start, y_end, color="blue", alpha=0.15)

plt.tight_layout()
plt.savefig("day15_heatmap.png", dpi=150)
plt.show()

# ============================================================
# PHASE 4: BUILDING THE 3-PANEL CHART (SIMPLE VERSION)
# ============================================================

# ---- STEP 1: subway entries for STN_003, hour by hour ----
station_column_name = "stn_003"  # change this if your cleaned id looks different

subway_hours = []
subway_entries = []

for hour in range(24):
    subway_hours.append(hour)
    if hour in day15_pivot.index:
        value = day15_pivot.loc[hour, station_column_name]
    else:
        value = 0  # no data for this hour
    subway_entries.append(value)

print("Subway entries by hour:", subway_entries)

# ---- STEP 2: scooter rides near STN_003, hour by hour ----
# STN_003 is located around (40.7128, -74.0060)
station_lat = 40.7128
station_lng = -74.0060
box_size = 0.006

min_lat = station_lat - box_size
max_lat = station_lat + box_size
min_lng = station_lng - box_size
max_lng = station_lng + box_size

near_station = scooter[
    (scooter["start_lat"] >= min_lat)
    & (scooter["start_lat"] <= max_lat)
    & (scooter["start_lng"] >= min_lng)
    & (scooter["start_lng"] <= max_lng)
    & (scooter["date"] == pd.to_datetime("2026-06-15").date())
]

print("Scooter rides near STN_003 on Day 15:", len(near_station))

near_station = near_station.copy()
near_station["hour"] = near_station["start_time"].dt.hour

scooter_hours = []
scooter_ride_counts = []

for hour in range(24):
    scooter_hours.append(hour)
    count_this_hour = len(near_station[near_station["hour"] == hour])
    scooter_ride_counts.append(count_this_hour)

print("Scooter rides by hour:", scooter_ride_counts)

# ---- STEP 3: precipitation for Day 15, using pd.read_json ----
# convert_dates=False stops pandas from GUESSING the date format on its own,
# which is risky here since the dates are written in two different styles
# (and pandas can silently misread "01-06-2026" as Jan 6 instead of Jun 1).
city = pd.read_json("city_heartbeat.json", convert_dates=False)
print(city)

city = city.T  # transpose so each row is one day
city = city.reset_index()
city = city.rename(columns={"index": "date_key"})
print(city.head())

# We use day_number (already in the data) instead of parsing the messy
# date strings ourselves — it's reliable no matter which date format was used.
day15_row = city[city["day_number"] == 15]
print(day15_row)

day15_weather = day15_row["weather"].values[0]
print(day15_weather)

rain_value = day15_weather["precipitation_mm"]
print("Day 15 precipitation raw value:", rain_value)

if isinstance(rain_value, str):
    if rain_value.lower() == "none":
        precipitation = 0.0
    elif "mm" in rain_value.lower():
        precipitation = float(rain_value.lower().replace("mm", ""))
    else:
        precipitation = 0.0  # e.g. "T-Storm" has no exact mm value
        print("Note: precipitation was listed as", rain_value, "- no exact mm value given")
else:
    precipitation = float(rain_value)

print("Day 15 precipitation (mm):", precipitation)

# ---- STEP 4: draw the 3 panels ----
fig, axes = plt.subplots(3, 1, sharex=True, figsize=(10, 8))

# Panel 1: subway entries
axes[0].plot(subway_hours, subway_entries, marker="o", color="blue")
axes[0].set_title("Subway Entries at STN_003 (Day 15)")
axes[0].set_ylabel("Entries")

# Panel 2: scooter rides
axes[1].bar(scooter_hours, scooter_ride_counts, color="orange")
axes[1].set_title("Scooter Rides Near STN_003 (Day 15)")
axes[1].set_ylabel("Number of Rides")

# Panel 3: precipitation (flat line — only a daily total is available)
axes[2].axhline(precipitation, color="green", linewidth=2)
axes[2].set_title("Precipitation on Day 15")
axes[2].set_ylabel("Precipitation (mm)")
axes[2].set_xlabel("Hour of Day")

# Shade the disputed 14:00-20:00 window on all 3 panels
for ax in axes:
    ax.axvspan(14, 20, alpha=0.2, color="red")

plt.tight_layout()
plt.savefig("stn003_case_file.png", dpi=150)
plt.show()
