# Week 3 — Python ETL, Pandas, and DuckDB

3주차 실습 코드와 산출물입니다. 고정 시드로 주문 데이터를 만들고, Pandas로 탐색·정제한 뒤 DuckDB로 CSV와 Parquet 데이터를 분석합니다.

## 학습 내용

- Pandas에서 행과 열 선택, 조건 필터링, 결측치 처리, 자료형 변환
- 파생 컬럼과 카테고리별 집계 만들기
- 주문 데이터 정제와 품질 검사
- CSV와 Parquet 읽기·쓰기 및 DuckDB SQL 분석
- Pandas와 DuckDB 결과 비교, 고객 데이터 결합
- 이벤트 데이터로 시계열 분석과 구매 퍼널 계산

## 준비

Python 3.12 이상을 권장합니다. `week3` 폴더에서 가상환경을 활성화한 뒤 필요한 패키지를 설치하세요.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install pandas numpy duckdb pyarrow
```

이미 가상환경을 만들었다면 첫 두 줄은 생략하고 활성화만 하면 됩니다.

## 실습 실행 흐름

명령은 모두 `week3` 폴더에서 실행합니다.

```bash
cd ~/data-eng/week3
source .venv/bin/activate
```

### 1. 주문 데이터 만들고 살펴보기

```bash
python make_orders.py
python transform.py
```

`make_orders.py`는 고정 시드로 1,000건의 주문을 만든 뒤 결측 30건, 카테고리 공백 20건, 중복 15건을 추가해 `orders.csv`를 저장합니다. `transform.py`는 행·열 선택, 필터링, 결측 처리, 날짜 변환과 `amount` 계산을 연습하고 `orders_step1.parquet`을 만듭니다.

### 2. 정제와 품질 리포트

```bash
python clean_orders.py
python quality_report.py
```

`clean_orders.py`는 DuckDB로 `orders.csv`를 읽고 Pandas로 카테고리 공백, 날짜 자료형, 중복 주문 ID, 가격 결측을 처리합니다. 검증을 통과하면 `orders_clean.parquet`을 저장합니다. `quality_report.py`는 전후 지표를 비교해 `quality_report.csv`를 만듭니다. 정리된 설명은 [`quality_report.md`](quality_report.md)에 있습니다.

> 원본의 주문 ID 컬럼명은 `orders_id`입니다. `transform.py`에서는 분석 편의를 위해 `order_id`로 이름을 바꿉니다.

### 3. Pandas 집계와 고객 결합

```bash
python make_customers.py
python analyze.py
python timeseries.py
```

`analyze.py`는 카테고리·월별 집계, 고객 데이터 결합, `pivot_table`과 데이터 형태 변환을 다룹니다. `timeseries.py`는 일별·주별·월별 매출과 이동 평균을 계산하고 `orders_enriched.parquet`을 저장합니다.

### 4. 대용량 이벤트 데이터와 DuckDB

```bash
python make_events.py
python query.py
python speed.py
python sql_analysis.py
python funnel.py
```

`make_events.py`는 100만 건의 이벤트를 만들어 `events.csv`로 저장합니다. `query.py`는 CSV를 직접 조회하고, `speed.py`는 `events.csv`를 `events.parquet`으로 변환하며 압축·조회 성능을 비교합니다. `sql_analysis.py`와 `funnel.py`에서는 DuckDB의 집계, 조인, 윈도 함수와 사용자별 조회·장바구니·구매 전환 분석을 연습합니다.

## 주요 파일

| 파일 | 설명 |
|---|---|
| `make_orders.py` | 고정 시드 주문 데이터 생성 |
| `transform.py` | Pandas 기본 변환 실습 |
| `clean_orders.py` | 주문 데이터 정제와 유효성 검사 |
| `quality_report.py` | 품질 지표 전후 비교 CSV 생성 |
| `quality_report.md` | 3주차 데이터 품질 리포트 |
| `make_customers.py`, `analyze.py` | 고객 데이터 생성 및 Pandas 분석 |
| `timeseries.py` | 주문 시계열 분석 |
| `make_events.py`, `query.py` | 이벤트 데이터 생성 및 DuckDB 기초 질의 |
| `speed.py` | CSV·Parquet 변환, 압축과 조회 성능 비교 |
| `sql_analysis.py`, `funnel.py` | DuckDB 심화 분석 및 구매 퍼널 |

## 생성 파일과 Git

실행하면 `.csv`와 `.parquet` 데이터 파일이 생성됩니다. `events.csv`는 100만 행 규모라 용량이 커질 수 있습니다. 데이터가 스크립트로 재생성 가능하고 크다면, 보통 코드와 문서만 Git에 올리고 생성 데이터는 제외합니다. 과제 제출에 결과 파일이 필요하면 해당 파일만 별도로 추가하세요.
