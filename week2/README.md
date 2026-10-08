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
