# 4단계: 순서를 바꾸면 결과가 달라지는지 확인

import pandas as pd
from clean_orders import load_raw
 
raw = load_raw()
 
# 순서 A — 중복 제거 후 중앙값
a = raw.copy()
a = a.drop_duplicates(subset='orders_id', keep='first')
med_a = a['price'].median()
 
# 순서 B — 중복이 있는 채로 중앙값
b = raw.copy()
med_b = b['price'].median()
 
print('순서 A 중앙값:', med_a)
print('순서 B 중앙값:', med_b)
print('같은가:', med_a == med_b)


