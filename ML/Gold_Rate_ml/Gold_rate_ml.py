import numpy as np     #numbers
import pandas as pd     #tables
import matplotlib.pyplot as plt     #charts
from sklearn.linear_model import LinearRegression   #ML Model
from sklearn.model_selection import train_test_split    #the split data
from sklearn.metrics import r2_score,mean_absolute_error #evaluation of model
from sklearn.preprocessing import PolynomialFeatures    #for the curved model later

gold_file = pd.read_csv("gold_rate.csv")
df = gold_file
print(f"No of rows: {len(df)}")
# print(df.head())
# print(df.describe())


plt.figure(figsize = (4,3))
plt.scatter(df["year"],df["gold_rate_pkr"],color = "blue") 
plt.xlabel("Year")
plt.ylabel("Gold rate (PKR per tola)")
plt.title("Gold rate over the years")
# plt.show()


X = df.drop(columns = ["gold_rate_pkr"]).values
Y = df["gold_rate_pkr"].values


X_train, X_test, Y_train, Y_test = train_test_split(X,Y,test_size = 0.25,random_state = 42)
print(f"X_train shape: {X_train.shape}")
print(f"X_test shape: {X_test.shape}")
print(f"Y_train shape: {Y_train.shape}")
print(f"Y_test shape: {Y_test.shape}")

model = LinearRegression()
model.fit(X_train,Y_train)

print("Training completed.")


line_years = np.array([[Y] for Y in range(2000, 2025)])
line_preds = model.predict(line_years)

plt.figure(figsize=(8, 5))
plt.scatter(df["year"], df["gold_rate_pkr"], color="#1E8E3E", label="Actual data")
plt.plot(line_years, line_preds, color="#C0392B", linewidth=2, label="Model's line")
plt.xlabel("Year")
plt.ylabel("Gold rate (PKR per tola)")
plt.title("Linear Regression fit")
plt.legend()
# plt.show()

print(X_test    )
Y_pred = model.predict(X_test)
print(Y_pred)
print(f"Mean Absolute Error: {mean_absolute_error(Y_test,Y_pred)}")
print(f"R2 Score: {r2_score(Y_test,Y_pred)}")

print(model.predict([[2029]] )) 

poly = PolynomialFeatures(degree=2,include_bias=False) 
X_poly = poly.fit_transform(X)


Xp_train, Xp_test, Yp_train, Yp_test = train_test_split(X_poly,Y,test_size = 0.25,random_state = 42)

model_poly = LinearRegression()
model_poly.fit(Xp_train,Yp_train)
print("Training completed for polynomial regression.")

print(f"Mean Absolute Error: {mean_absolute_error(Yp_test,model_poly.predict(Xp_test))}")
print(f"R2 Score: {r2_score(Yp_test,model_poly.predict(Xp_test))}")
