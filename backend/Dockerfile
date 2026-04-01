FROM python:3.11-slim

WORKDIR /app

# 先複製 requirements
COPY requirements.txt ./

# 👉 一次安裝所有套件（包含 openai）
RUN pip install --no-cache-dir -r requirements.txt

# 複製程式碼
COPY . .

EXPOSE 8000