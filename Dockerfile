FROM python:3.10-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# 复制项目文件
COPY . .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 创建必要的目录
RUN mkdir -p files/pdf_files files/json_files files/backup_files

# 暴露端口
EXPOSE 8080

# 设置环境变量
ENV PYTHONUNBUFFERED=1

# 启动命令
CMD ["streamlit", "run", "Assistant.py", "--server.port=8080", "--server.address=0.0.0.0"] 