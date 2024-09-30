import pandas as pd

# 讀取Excel文件
file_path = 'competitions/甲場地表.xlsx'  # 將此路徑替換為實際文件路徑
df = pd.read_excel(file_path)

# 顯示表格內容
print(df)
