import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error

# SECTION 1
df = pd.read_csv(r"D:\AtomCamp\Machine Learning\Practice Assignment\stock_market_data (1).csv")
df['Date'] = pd.to_datetime(df['Date'])
print(df.head())
print(df.shape)
print(df.dtypes)
print(df["Ticker"].unique())

one_stock = df[df["Ticker"] == "AAPL"].copy()
one_stock = one_stock.sort_values(by="Date")

plt.plot(one_stock["Date"], one_stock["Close"], color="blue")
plt.xlabel("Date"); plt.ylabel("Close Price")
plt.title("AAPL Stock Price Over Time")
# plt.show()

# SECTION 2
one_stock["Next_Close"] = one_stock["Close"].shift(-1)
one_stock = one_stock.iloc[:-1]   # drop last row, no "tomorrow" for it
print(one_stock.head())

# SECTION 3
one_stock["Percentage_change"] = ((one_stock["Close"] - one_stock["Close"].shift(1)) / one_stock["Close"].shift(1)) * 100
one_stock["MA_5"] = one_stock["Close"].rolling(window=5).mean()
one_stock["Previous_Close"] = one_stock["Close"].shift(1)
one_stock = one_stock.dropna()
print(one_stock.head(10))


X = one_stock[["Percentage_change", "Previous_Close", "MA_5"]]
Y = one_stock["Next_Close"]


X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.20, shuffle=False)

print(f"X_train shape: {X_train.shape}")
print(f"X_test shape: {X_test.shape}")
print(f"Y_train shape: {Y_train.shape}")
print(f"Y_test shape: {Y_test.shape}")

model = LinearRegression()
model.fit(X_train, Y_train)
print("Training completed.")

y_pred = model.predict(X_test)



results = pd.DataFrame({
    "Date": one_stock.loc[X_test.index, "Date"].values,
    "Actual": Y_test.values,
    "Predicted": y_pred
})
print(results.head(10))

plt.figure(figsize=(10, 5))
plt.plot(results["Date"], results["Actual"], label="Actual", color="blue")
plt.plot(results["Date"], results["Predicted"], label="Predicted", color="orange")
plt.xlabel("Date"); plt.ylabel("Next Close Price")
plt.title("AAPL: Actual vs Predicted Next Close")
plt.legend()
plt.show()

mae = mean_absolute_error(Y_test, y_pred)
rmse = np.sqrt(((Y_test - y_pred) ** 2).mean())
r2 = r2_score(Y_test, y_pred)

print(f"\nMAE:  {mae:.2f}")
print(f"RMSE: {rmse:.2f}")
print(f"R2 Score: {r2:.4f}")