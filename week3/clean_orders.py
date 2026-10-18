# # clean_ordrs.py = DuckDB ㅊ추출 + Pandas 정제 파이프라인
# import duckdb
# import pandas as pd
#
# def load_raw() -> pd.DataFrame:
#     # 추출 - 대용량이어도 여기서 필터, 열 선택으로 줄일 수 있다.
#     return duckdb.sql("SELECT * FROM 'orders.csv'").df()
#
#
# def clean(df: pd.DataFrame) -> pd.DataFrame:
#     out = df.copy()
#     out['category'] = out['category'].str.strip()  # 공백 오염 제거
#     out['order_date'] = pd.to_datetime(out['order_date'])  # 타입 복원
#     out = out.drop_duplicates(subset='orders_id', keep='first')  # 중복 제거
#     out['price'] = out['price'].fillna(out['price'].median())  # 결측 보정
#     out['amount'] = out['price'] * out['quantity']  # 파생 컬럼
#     return out
#
#
# if __name__ == '__main__':
#     raw = load_raw()
#     cleaned = clean(raw)
#     cleaned.to_parquet('orders_clean.parquet', index=False)
#     print(len(raw), '행 ->', len(cleaned), '행 정제 완료')
#
#

# clean_orders.py 최종본 — 2단계 파일을 통째로 이 내용으로 바꿉니다(검증까지 포함)
import duckdb
import pandas as pd

VALID_CATEGORIES = ['식품', '가전', '의류', '도서']


def load_raw() -> pd.DataFrame:
    return duckdb.sql("SELECT * FROM 'orders.csv'").df()


def clean(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out['category'] = out['category'].str.strip()
    out['order_date'] = pd.to_datetime(out['order_date'])
    out = out.drop_duplicates(subset='orders_id', keep='first')
    out['price'] = out['price'].fillna(out['price'].median())
    out['amount'] = out['price'] * out['quantity']
    return out


def validate(df: pd.DataFrame) -> dict:
    return {
        'price_le_0':    int((df['price'] <= 0).sum()),
        'quantity_le_0': int((df['quantity'] <= 0).sum()),
        'unknown_cat':   int((~df['category'].isin(VALID_CATEGORIES)).sum()),
        'dup_order_id':  int(df['orders_id'].duplicated().sum()),
        'null_price':    int(df['price'].isna().sum()),
    }


if __name__ == '__main__':
    raw = load_raw()
    cleaned = clean(raw)
    issues = validate(cleaned)

    if any(v > 0 for v in issues.values()):
        print('검증 실패:', issues)
        raise SystemExit(1)          # 1-2에서 배운 종료 코드

    cleaned.to_parquet('orders_clean.parquet', index=False)
    print(len(raw), '행 ->', len(cleaned), '행 정제 완료 (검증 통과)')
