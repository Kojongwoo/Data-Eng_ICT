import pandas as pd

df = pd.read_csv('orders.csv')

print(df.shape)
print(df.dtypes)
print(df.head(3))
df.info()
print(df.describe())

# price -> 정수만 있는데 float64
print('price dtype :', df['price'].dtype)
print('quantity dtype:', df['quantity'].dtype)

# 이유: 결측 때문
print('price 결측 :', df['price'].isna().sum())
print('quantity 결측 :', df['quantity'].isna().sum())

# 1000 -> 1000.0
print(df['price'].head(3).tolist())

# Parquet
df.to_parquet('orders_raw.parquet', index=False)

import os
csv_size = os.path.getsize('orders.csv')
pq_size = os.path.getsize('orders_raw.parquet')
print(f'CSV    : {csv_size:,} bytes')
print(f'Parquet: {pq_size:,} bytes  ({pq_size / csv_size:.0%})')

# 필요한 열만 읽기
# Parquet: 2열만 읽는다
slim = pd.read_parquet('orders_raw.parquet', columns=['category', 'price'])
print(slim.shape)
print(slim.columns.tolist())

# CSV: usecols로 지정해도 파일 전체는 읽어야 합니다
slim_csv = pd.read_csv('orders.csv', usecols=['category', 'price'])
print(slim_csv.shape)

