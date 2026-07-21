# 📊 Exploratory Data Analysis Projects

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white" />
  <img src="https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy&logoColor=white" />
  <img src="https://img.shields.io/badge/Matplotlib-11557C?style=flat-square" />
  <img src="https://img.shields.io/badge/Seaborn-3776AB?style=flat-square" />
</p>

A collection of exploratory data analysis (EDA) projects, each digging into a different dataset — cleaning raw data, handling missing values and outliers, and building visualizations to uncover patterns, relationships, and insights.

**Common workflow across every project:**
1. Load and inspect the raw dataset (structure, types, missing values)
2. Clean the data — handle nulls, fix inconsistent formatting, treat outliers
3. Engineer/derive features where useful
4. Visualize distributions, relationships, and trends
5. Interpret findings and document key takeaways

---

## 📁 Projects

### 🚕 Uber Rides EDA
Analysis of ride-hailing data covering booking status, vehicle types, payment methods, and cancellation patterns.
- Cleaned structurally-missing columns (cancellation/incomplete-ride fields that only apply to specific booking statuses)
- Distribution analysis on fare, ride distance, and VTAT/CTAT timing metrics
- Time-based analysis: hourly ride demand, daily trends, day-of-week patterns
- Correlation analysis across all numeric fields
- Categorical breakdowns: booking status, vehicle type, payment method, cancellation reasons

### ⚽ FIFA EDA
Exploratory analysis of player and match data from FIFA, examining performance metrics, player attributes, and comparative statistics.
- Data cleaning and preprocessing of player/team attributes
- Distribution and outlier analysis on key performance stats
- Comparative visualizations across positions, clubs, and nationalities
- Correlation analysis between player attributes and overall ratings

### 🚢 Titanic EDA
Classic survival-analysis dataset — exploring what factors influenced passenger survival aboard the Titanic.
- Missing value treatment (Age, Cabin, Embarked)
- Feature engineering: Family Size, Alone/Not Alone indicator
- Outlier detection and treatment on Fare (skew correction via clipping/log transform)
- Survival analysis by passenger class, gender, age group, and family size
- Heatmaps and grouped visualizations to compare survival rates across categories

### 🦠 COVID-19 EDA
Time-series analysis of the global COVID-19 pandemic spread using daily country-level case data.
- Global and per-country trend analysis (Confirmed, Deaths, Recovered, Active)
- Daily new case calculation from cumulative totals
- WHO Region-level comparisons
- Correlation analysis between case metrics
- Geographic visualization (choropleth mapping) of confirmed cases by country

### 🚇 Subway Station EDA
Exploratory analysis of subway station data, examining ridership, station characteristics, and usage patterns.
- Data cleaning and preprocessing of station-level records
- Distribution analysis of ridership/usage metrics
- Comparative visualizations across stations/lines
- Pattern and trend identification in station usage

---

## 🛠️ Tools & Libraries

- **Python** — core language for all analysis
- **Pandas** — data cleaning, wrangling, and aggregation
- **NumPy** — numerical operations and array handling
- **Matplotlib** — base plotting and chart customization
- **Seaborn** — statistical visualizations (distributions, heatmaps, categorical plots)

---

## 🗂️ Repo Structure

```
.
├── uber-eda/
├── fifa-eda/
├── titanic-eda/
├── covid19-eda/
├── subway-station-eda/
└── README.md
```

Each folder contains the dataset (or a link to its source), the analysis notebook/script, and generated visualizations.

---

## 💡 What I Learned

Working across five very different datasets — ride-hailing, sports, survival analysis, pandemic time-series, and transit data — helped me build a repeatable EDA process: spotting structural vs. random missingness, choosing the right cleaning technique for each situation (drop, impute, clip, transform), and picking the visualization that actually answers the question instead of just looking impressive. Each dataset came with its own quirks, and working through them sharpened how I read a boxplot, a correlation matrix, or a time-series trend before jumping to conclusions.

---

## 👤 About Me

**Abdullah Alam Ansari**
BS Computer Science, GIK Institute of Engineering Sciences and Technology (GIKI)

<p align="center">Learning in public, one dataset at a time 📈</p>
