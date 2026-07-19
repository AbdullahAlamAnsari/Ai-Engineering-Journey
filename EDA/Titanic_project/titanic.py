import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns


titanic_data = pd.read_csv("titanicdata.csv")

#getting the feel of data

print(titanic_data.head())
