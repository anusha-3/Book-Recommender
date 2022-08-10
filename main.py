import csv
import pandas as pd
# with open('raw_data.csv', 'r') as df:
#     popular_df = csv.reader(df, delimiter=' ')
#     Output = []
#     for row in popular_df:
#         Output.append(row[:])
# print(popular_df)

df = pd.read_csv('raw_data.csv')
Book_name = df['Book-Title'].tolist()
print(Book_name)