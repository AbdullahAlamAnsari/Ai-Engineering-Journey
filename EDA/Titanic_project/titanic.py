import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns


titanic_data = pd.read_csv("titanic.csv")

#getting the feel of data

print(titanic_data.head(5))

#checking null values

print(titanic_data.isnull().sum())
print(f"Total data entries: {len(titanic_data)}")

sns.catplot(x = 'Sex',hue = 'Survived',data = titanic_data,kind = 'count')
plt.show()
plt.savefig("catplot - sex")

# the survival rate of men is around 20% and that of women is around 75%


group = titanic_data.groupby(['Pclass', 'Survived'])
pclass_survived = group.size().unstack()
sns.heatmap(pclass_survived, annot = True, fmt ="d")
plt.show()
plt.savefig("heatmap - pclass & survived")

# Class 1 passengers have a higher survival chance compared to classes 2 and 3


sns.violinplot(x ="Sex", y ="Age", hue ="Survived", 
data = titanic_data, split = True)
plt.show()
plt.savefig("Violin - sex vs age")

# Good for children.
# High for women in the age range 20-50.
# Less for men as the age increases.

titanic_data['Family_Size'] = titanic_data["SibSp"] + titanic_data["Parch"]
print(titanic_data["Family_Size"])

titanic_data['Alone'] = 0
titanic_data.loc[titanic_data['Family_Size'] == 0, 'Alone'] = 1
print(titanic_data['Alone'])    

# Line plot for Family
sns.lineplot(x ='Family_Size', y ='Survived', data = titanic_data)
plt.show()
plt.savefig("Family_Size vs Survived")
# Line for Alone
sns.lineplot(x ='Alone', y ='Survived', data = titanic_data)
plt.savefig("Alone vs survived")
plt.show()

# If a passenger is alone, the survival rate is less.
# If the family size is greater than 5, chances of survival decrease considerably.


titanic_data['Fare_Range'] = pd.qcut(titanic_data['Fare'], 4)


# Barplot - Shows approximate values based 
# on the height of bars.
sns.barplot(x ='Fare_Range', y ='Survived', 
data = titanic_data)
plt.savefig("fair price vs age")
plt.show()

# It can be concluded that if a passenger paid a higher fare, the survival rate is more.

sns.catplot(x ='Embarked', hue ='Survived', 
kind ='count', col ='Pclass', data = titanic_data)
plt.show()
plt.savefig("Embarkment - Pclass vs Survied")


# Majority of the passengers boarded from S. So, the missing values can be filled with S.
# Majority of class 3 passengers boarded from Q.
# S looks lucky for class 1 and 2 passengers compared to class 3.

