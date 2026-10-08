# Week 2 실습

데이터베이스 활용과 데이터 수집·적재 기초를 실습한 내용입니다.

## 학습 내용

- **MySQL**: CTE(`WITH`), 윈도우 함수(`LAG()`)
- **MongoDB**: 접속 로그 생성 및 적재
- **웹 크롤링**: 페이지 요청, HTML 파싱, 다음 페이지 처리, MySQL 적재

## 주요 파일

- `memo.txt`: 수업 내용 메모
- `fetch_one.py`, `fetch_raw.py`, `check_robots.py`: 요청과 크롤링 기초
- `selector_test.py`, `safe_pick.py`, `next_page.py`: HTML 선택자와 페이지 탐색 연습
- `crawler_pipeline.py`: 수집 → 파싱 → MySQL 적재 흐름
- `load_logs.py`: MongoDB에 테스트 로그 적재
- `day4_ERD.png`: ERD 실습 자료
- `PDF/`: 주차별 수업 자료


# 2주차 산출물 — 쇼핑몰 ERD 설계 + 크롤링 파이프라인

## 1. ERD 설계서
- 파일: ERD_설계서.md (엔터티 정의 · 관계 · 정규화 근거 · 반정규화 결정)
- 표 4개: customers · products · orders · order_items
- N:M(주문↔상품)을 order_items 교차 표로 해소

## 2. 크롤러
- 대상: https://quotes.toscrape.com (수집 허용 확인 완료)
- 구조: fetch(수집) → parse(정제) → load(적재) 3함수 분리
- 예절: User-Agent 표기 · 요청 간격 1초 · robots.txt 사전 확인
- 중복 방지: quotes 표의 UNIQUE(author, quote_text) 제약 + INSERT IGNORE

## 3. 실행 방법
```
docker start de-mysql
python3 -m venv .venv && source .venv/bin/activate   # Windows(WSL2)·macOS·리눅스 모두 같습니다
pip install requests beautifulsoup4 pymysql
python3 check_robots.py       # 수집 가능 여부 확인
python3 crawler_pipeline.py   # 3페이지 수집·적재
```

## 4. 검증한 것
- 첫 실행: parsed 10 / saved 10 × 3페이지 = 30건
- 재실행: parsed 10 / saved 0 (DB 제약이 중복을 막음)
- SELECT COUNT(*) FROM quotes → 30

## 5. 남은 개선점
- tags를 쉼표 문자열로 저장 중 (1NF 위반) → quote_tags 교차 표로 분리 예정
- 주차별 개선점 

Week2: Database
1. day01: Install MySQL 8.0 & Basic Query Practice
대학교에서 데이터베이스 이론을 배우고 sqld 자격증을 취득한 경험이 있어 비교적 수월했던 하루

2. day02: CTE, Window Function
이론으로만 배웠었던 윈도우 함수를 직접 작성해보니 어려웠다. 
다중 서브쿼리를 With 절로 한번에 작성하는 것이 다중 쿼리를 해석하는 것보다 수월했다.

3. day03: MongoDB & 비정형 데이터
가장 생소했던 내용이다. 비정형 데이터를 처음 다루어 봤고, 말로만 듣던 MongoDB를 처음 접했던 날이었다.

4. day04: ERD 설계 및 정규화/반정규화
데이터베이스 이론에서 배웠던 정규화, 반정규화 이론을 실습에 적용해 이해를 빨리할 수 있었다.
개체-관계 다이어그램을 직접 그려봄으로써 데이터베이스의 구조를 이해하는 데 도움이 되었다.

5. day05: Python 기반의 크롤러
크롤링은 처음 해봐서 생소했다. 크롤링 한 데이터를 미리 구축한 파이프라인에 적재하는 과정에서 데이터 엔지니어링의 첫 걸음을 내딛은 거 같았다.

