# 1단계: 빌드 전용
FROM python:3.12 AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --target=/deps -r requirements.txt

# 2단계: 실행용
FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /deps /deps
ENV PYTHONPATH=/deps
COPY . .
CMD ["python", "app.py"]
