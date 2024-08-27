import pandas as pd
import os
# filepath = os.path.join('./competitions', 'text.xlsx')
filepath = "./competitions/test.xlsx"    
df = pd.read_excel(filepath)

# 查找第6行（索引5）沒有內容的第一列
row = df[(df.iloc[:, 4].isna()) | (df.iloc[:, 5].isna())].iloc[0]
print(row)