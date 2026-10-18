import pandas as pd

df = pd.read_parquet('orders_step1.parquet')
customers = pd.read_csv('customers.csv', parse_dates=['joined'])

# 2단계: 카테고리별 명명 집계
summary = df.groupby('category').agg(
    orders=('order_id', 'count'),
    total=('amount', 'sum'),
    avg_price=('price', 'mean'),
).round(0).sort_values('total', ascending=False)
print(summary)
print('열 이름:', summary.columns.tolist())

# 3단계 여러 기준으로 묶기
by2 = df.groupby(['category', 'month']).agg(
    orders=('order_id', 'count'),
    total=('amount', 'sum'),
)
print(by2.head(6))

# 다루기 쉽게 평탄화
flat = by2.reset_index()
print(flat.head(3))
print('행 수:', len(flat))

#4단계: 주문과 고객 결합
m = df.merge(customers, on='customer_id', how='left', validate='many_to_one')
print('결합 전:', len(df), '행 / 결합 후:', len(m), '행')
print('region 결측:', m['region'].isna().sum(), '건')

#5단계: 행 불어나게 하기
# 고객 마스터에 중복 행 심기
bad = pd.concat([customers, customers.head(5)], ignore_index=True)
print('customers 원본:', len(customers), '/ 중복 심은 것: ', len(bad))

# validate 없이 - 조용히 불어남
m_bad = df.merge(bad, on='customer_id', how='left')
print('결합 후 행 수:', len(m_bad), '(원본', len(df), ')')
print('매출 합계 원본:', int(df['amount'].sum()))
print('매출 합계 결합 후:', int(m_bad['amount'].sum()), '<- 부풀려졌습니다')

# 5단계(validate) — analyze.py 끝에 이어 붙입니다
# validate를 주면 여기서 멈춥니다
try:
    df.merge(bad, on='customer_id', how='left', validate='many_to_one')
except Exception as e:
    print('예상대로 차단:', type(e).__name__)
    print(e)

# 5단계(습관) — analyze.py 끝에 이어 붙입니다
# 결합 전에 키 중복을 미리 확인하는 습관
print('오른쪽 키 중복 건수:', bad['customer_id'].duplicated().sum())
print('정상 마스터 중복 건수:', customers['customer_id'].duplicated().sum())

#6단계: 지역 x 카테고리 교차표
pv = m.pivot_table(index='region', columns='category', values='amount', aggfunc='sum', fill_value=0)
print(pv)
print('교차표 총합 == 전체 매출:', pv.to_numpy().sum() == m['amount'].sum())

# 6단계(다른 관점) — analyze.py 끝에 이어 붙입니다
# 건수로 채운 교차표 · 평균으로 채운 교차표
print(m.pivot_table(index='region', columns='category',
                    values='order_id', aggfunc='count', fill_value=0))
print(m.pivot_table(index='region', columns='category',
                    values='amount', aggfunc='mean', fill_value=0).round(0))

#7단계 - 긴 형태와 넓은 형태 오가기
# 넓은 형태(교차표) -> 긴 형태
long = pv.reset_index().melt(id_vars='region', var_name='category', value_name='amount')
print(long.head())
print('행 수:', len(long), '(지역 4 x 카테고리 4)')

# 긴 형태 -> 다시 넓게
wide = long.pivot(index='region', columns='category', values='amount')
print('원래대로 돌아왔는가:', wide.equals(pv))