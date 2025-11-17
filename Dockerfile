# Dockerfile for IndexTTS with GPU H100 support
# 基于CUDA-enabled Python镜像，支持H100 GPU

FROM nvidia/cuda:12.2.2-devel-ubuntu22.04

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3.11-dev \
    python3-pip \
    git \
    build-essential \
    libsndfile1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# 设置Python别名
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1 && \
    update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1

# 升级pip
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# 复制依赖文件
COPY 1.txt requirements.txt ./

# 安装Python依赖
RUN pip install --no-cache-dir -r 1.txt || true

# 复制应用代码
COPY . .

# 设置环境变量
ENV PYTHONUNBUFFERED=1
ENV GRADIO_SERVER_NAME=0.0.0.0
ENV GRADIO_SERVER_PORT=7860
ENV HF_HOME=/app/hf_cache
ENV TORCH_HOME=/app/torch_cache

# 创建缓存目录
RUN mkdir -p /app/hf_cache /app/torch_cache /app/checkpoints

# 暴露端口
EXPOSE 7860

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:7860')" || exit 1

# 启动应用
CMD ["python", "webui.py", "--host", "0.0.0.0", "--port", "7860"]
