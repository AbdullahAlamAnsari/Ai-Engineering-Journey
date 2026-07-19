import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error
from sklearn.preprocessing import PolynomialFeatures    #for the curved model later
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

house_data = pd.read_csv("D:\AtomCamp\Machine Learning\house_price_ml\house_price_prediction_dataset.csv")


#SECTION - 1

print(house_data.head())
print(house_data.shape)
print(house_data.dtypes)
print(house_data.describe(include="all"))

#SECTION - 2

print(f"Number of missing values: {house_data.isnull().sum().sum()}")
# 1- no missing values 
# 2- Price in usd is my target var since we want to predict it - Y
# 3-Age_years Garage Bedrooms Bathroom and Area sq all can be X since all can impact our Y in the end
Y = house_data["Price_USD"]
print(f"Prices in usd:\n {Y.head()}")


house_data["Price_per_sqft"] = house_data["Price_USD"] / house_data["Area_sqft"]
print(house_data.head())

X = house_data[["Area_sqft","Bedrooms","Bathrooms","Age_years","Garage"]]
print(f"X values:\n{X}")

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.20, random_state=42)

model = LinearRegression()
model.fit(X_train, Y_train)
print("Training completed.")


y_pred = model.predict(X_test)
df = pd.DataFrame({
    "Area_sqft": [2200],
    "Bedrooms": [4],
    "Bathrooms": [3],
    "Age_years": [6],
    "Garage": [1]
})
y_price = model.predict(df)
print(f"Price of the given data: {y_price}")
y_price = model.predict(df)
mae = mean_absolute_error(Y_test, y_pred)
rmse = np.sqrt(((Y_test - y_pred) ** 2).mean())
r2 = r2_score(Y_test, y_pred)



print(f"\nMAE:  {mae:.2f}")
print(f"RMSE: {rmse:.2f}")
print(f"R2 Score: {r2:.4f}")


#SECTION 8
print(f"Price of the given data: {y_price}")

plt.figure(figsize=(8, 6))
plt.scatter(Y_test, y_pred, alpha=0.6, color="steelblue")

# perfect prediction reference line (diagonal)
plt.plot([Y_test.min(), Y_test.max()], [Y_test.min(), Y_test.max()], color="red", linewidth=2)

plt.xlabel("Actual Price")
plt.ylabel("Predicted Price")
plt.title("Actual vs Predicted House Prices")
plt.show()


poly = PolynomialFeatures(degree=2,include_bias=False) 
X_poly = poly.fit_transform(X)


Xp_train, Xp_test, Yp_train, Yp_test = train_test_split(X_poly,Y,test_size = 0.20,random_state = 42)

model_poly = LinearRegression()
model_poly.fit(Xp_train,Yp_train)
print("Training completed for polynomial regression.")

print(f"Mean Absolute Error: {mean_absolute_error(Yp_test,model_poly.predict(Xp_test))}")
print(f"R2 Score: {r2_score(Yp_test,model_poly.predict(Xp_test))}")

#polynomial aint a good option



poly_pred = model_poly.predict(Xp_test)

plt.figure(figsize=(8, 6))
plt.scatter(Yp_test, poly_pred, alpha=0.6, color="seagreen")

# perfect prediction reference line (diagonal)
plt.plot([Yp_test.min(), Yp_test.max()], [Yp_test.min(), Yp_test.max()], color="red", linewidth=2)

plt.xlabel("Actual Price")
plt.ylabel("Predicted Price")
plt.title("Polynomial Regression: Actual vs Predicted House Prices")
plt.show()



# Turn continuous price into a binary category:
# 1 = above median price ("expensive"), 0 = at/below median ("not expensive")
median_price = house_data["Price_USD"].median()
house_data["Expensive"] = (house_data["Price_USD"] > median_price).astype(int)

Y_class = house_data["Expensive"]

X_train, X_test, Y_train, Y_test = train_test_split(X, Y_class, test_size=0.20, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
print("Scaling done ✅")

model = LogisticRegression(max_iter=2000)
model.fit(X_train_scaled, Y_train)
print("Model trained ✅")

y_pred = model.predict(X_test_scaled)

print(f"Accuracy: {accuracy_score(Y_test, y_pred):.4f}")
