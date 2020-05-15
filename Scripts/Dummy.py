import xlrd
import pandas as pd

csv_path = "/home/kevin/Seafile/Universität/6. Semester/Bachelor Arbeit/GEO data list.xlsx"

df = pd.read_excel(csv_path, index_col=[0])

print(df)

df.to_csv('/home/kevin/dummy.csv')
