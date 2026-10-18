import pandas as pd

df = pd.read_parquet('orders_step1.parquet')
customers = pd.read_csv('customers.csv', parse_dates=['joined'])
m = df.merge(customers, on='customer_id', how='left', validate='many_to_one')

# 일부러 실패 - 인덱스가 날짜가 아닌 채로 resample
# try:
#     m['amount'].resample('D').sum()
# except TypeError as e:
#     print('예상대로 실패:', e)

# 1단계 — timeseries.py 끝에 이어 붙입니다
ts = m.set_index('order_date').sort_index()
print('인덱스 타입:', ts.index.dtype)
print('기간:', ts.index.min().date(), '~', ts.index.max().date())
print(ts.head(2))

# 2단계 - timeseries.py 끝에 이어 붙임
daily = ts['amount'].resample('D').sum()
weekly_trend = daily.rolling(7).mean()

print('일별 매출 (첫 3일)')
print(daily.head(3))
print('7일 이동 평균 (마지막 3일)')
print(weekly_trend.round(0).tail(3))

print('daily 행 수:', len(daily))
print('rolling 행 수:', len(weekly_trend), '<- daily, rolling 행 수는 같습니다')

print(weekly_trend.head(8))

# 3단계: 주, 월별로 접어보기
weekly = ts['amount'].resample('W').sum()
monthly = ts['amount'].resample('ME').agg(['sum', 'mean', 'count'])

print('\n주별 매출')
print(weekly)
print('\n월별 요약')
print(monthly.round(0))

# 4단계: 기초 통계
print(m[['price', 'quantity', 'amount']].describe().round(0))

# 분위수로 분포 보기
print('\n주문 금액 분위수')
print(m['amount'].quantile([0.25, 0.5, 0.75, 0.9, 0.99]).round(0))

# 지역별 평균과 편차
print('\n지역별')
print(m.groupby('region')['amount'].agg(['mean', 'std', 'count']).round(0))

# 5단계: 분석 테이블 저장
m.to_parquet('orders_enriched.parquet', index=False)
print('저장 완료:', len(m), '행', len(m.columns), '열')
print('열 목록:', m.columns.tolist())

# 6단계 - 미니과제:
# 고객 별 집계 만들기 <주문 수, 총 구매액, 마지막 주문일, 상위 10명>

# 요일 별 평균 매출: 3-1의 weekday 열 활용

# 지역 별 가장 많이 팔린 카테고리: groupby 2번, 또는 2-2의 순위 발상

