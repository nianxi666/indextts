FROM python:3.10-slim

# 安装系统依赖（TTS 需要 ffmpeg、git 等）
RUN apt-get update && apt-get install -y \
    git \
    ffmpeg \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 克隆 Hugging Face Space 仓库（直接到当前目录）
RUN git clone https://huggingface.co/spaces/IndexTeam/IndexTTS-2-Demo .

# 安装 Python 依赖（使用克隆后的 requirements.txt）
RUN pip install --no-cache-dir -r requirements.txt

# 暴露 Gradio 默认端口
EXPOSE 7860

# 启动 Web UI
CMD ["python", "webui.py", "--server_name", "0.0.0.0", "--server_port", "7860"]
