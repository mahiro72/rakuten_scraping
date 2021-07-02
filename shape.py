import pandas as pd

data = pd.read_csv('test_csv.csv')
print(len(data["施設ID"].unique()))
print(data.shape)
