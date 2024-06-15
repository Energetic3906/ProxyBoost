# 使用更小的基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 复制代码文件到工作目录
COPY main.py .

# 安装依赖项并清理缓存
RUN pip install --no-cache-dir requests && \
    rm -rf /var/lib/apt/lists/*

EXPOSE 30830
# 运行代理服务器
CMD ["python", "main.py"]