import pandas as pd

data = pd.read_table(r"C:\Users\mahir\デスクトップ\ジョイリデータ\data\travel_20200131\02_Travel_HotelMaster.tsv\02_Travel_HotelMaster.tsv")
print(data.shape)
print(len(list(data["施設ID"].unique())))


