# 使用更小的基础镜像
FROM python:3.11-alpine

# 复制代码文件到工作目录
COPY main.py /app/

# 设置工作目录
WORKDIR /app

# 安装依赖项
RUN pip install --no-cache-dir \
        requests \
        beautifulsoup4

# 暴露端口
EXPOSE 30830
# 运行代理服务器
CMD ["python", "main.py"]