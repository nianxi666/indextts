# Koyeb部署指南

本项目配置已准备好部署到Koyeb。请按照以下步骤进行部署。

## 部署前准备

### 1. 配置文件
已为您配置了以下文件：
- `runtime.txt` - Python 3.10.13
- `requirements.txt` - 项目依赖
- `koyeb.yml` - Koyeb构建配置
- `.koyeb-deploy.yaml` - GPU部署配置（A4000）

### 2. 分支信息
- 当前分支：`koyeb-deploy-gpu-a4000-github-define-python`
- 部署将使用此分支的代码

## 部署步骤

### 方法1：使用Koyeb Web控制面板

1. 访问 https://app.koyeb.com
2. 登录您的Koyeb账户
3. 点击 "Create Service"
4. 选择 "GitHub" 作为源
5. 选择此仓库和 `koyeb-deploy-gpu-a4000-github-define-python` 分支
6. 配置服务：
   - **Name**: indextts-webui
   - **Builder**: Buildpack
   - **Python Version**: 3.10.13
   - **Run command**: `python webui.py --host 0.0.0.0 --port $PORT`
   - **Port**: 7860

7. 配置资源（Resources）：
   - **GPU**: NVIDIA A4000
   - **vCPU**: 4
   - **Memory**: 16GB

8. 环境变量：
   ```
   GRADIO_SHARE=false
   HF_HOME=/workspace/.huggingface
   TRANSFORMERS_CACHE=/workspace/.cache/transformers
   ```

9. 点击 "Deploy" 开始部署

### 方法2：使用Koyeb CLI

如果您已安装Koyeb CLI：

```bash
# 登录
koyeb login --token YOUR_API_TOKEN

# 部署
koyeb apps create indextts-webui \
  --git your-github-repo-url \
  --git-branch koyeb-deploy-gpu-a4000-github-define-python \
  --builder buildpack \
  --buildpack-python-version 3.10.13 \
  --port 7860 \
  --gpu a4000 \
  --cpu 4 \
  --memory 16Gi \
  --env GRADIO_SHARE=false \
  --env HF_HOME=/workspace/.huggingface \
  --env TRANSFORMERS_CACHE=/workspace/.cache/transformers
```

## 部署后

1. 部署完成后，Koyeb会为您的应用分配一个公开URL
2. 访问该URL即可使用IndexTTS WebUI
3. 首次启动时，模型会自动从Hugging Face下载

## 常见问题

### Q: 为什么需要GPU？
A: IndexTTS2引擎需要GPU加速进行文本转语音推理，A4000 GPU提供了很好的性能与成本平衡。

### Q: 模型下载需要多长时间？
A: 首次启动需要从Hugging Face下载模型检查点，这可能需要5-15分钟，取决于网络速度。

### Q: 如何更新代码？
A: 只需在此分支 (`koyeb-deploy-gpu-a4000-github-define-python`) 上推送更新，Koyeb会自动重新部署。

### Q: 如何查看日志？
A: 在Koyeb控制面板中，进入您的服务，点击 "Logs" 标签查看实时日志。

## 技术栈

- **框架**: Gradio (Python Web UI)
- **TTS引擎**: IndexTTS2
- **依赖**: 见 `requirements.txt`
- **Python版本**: 3.10.13
- **GPU**: NVIDIA A4000

## 需要帮助？

- Koyeb文档: https://koyeb.com/docs
- 本项目仓库: https://github.com/your-username/your-repo
- IndexTTS2: https://github.com/InternLM/IndexTTS2

---

部署密钥: rocrorea70dhiis0zw0u68j35xve4ljjpt6ytw2sz7ixbr8y70ox7dpgqj497h28
