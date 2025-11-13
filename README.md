# IndexTTS WebUI

一个基于Gradio的零样本文本转语音（TTS）Web界面，采用IndexTTS2引擎，支持多语言、情感控制等功能。

## 快速开始

### 本地运行
```bash
pip install -r requirements.txt
python webui.py
```

### Koyeb云部署
此项目已配置为可直接部署到Koyeb。所有必需的配置文件都已准备好。

**部署分支**: `koyeb-deploy-gpu-a4000-github-define-python`

**部署配置**:
- Python版本: 3.10.13
- GPU: NVIDIA A4000
- CPU: 4核
- 内存: 16GB
- Web框架: Gradio

**快速部署指南**: 查看 [KOYEB_QUICK_START.md](KOYEB_QUICK_START.md)

## 项目特性

- 🎤 **零样本TTS**: 使用参考音频进行语音合成
- 🗣️ **多语言支持**: 支持中文和英文
- 😊 **情感控制**: 支持参考音频、向量和文本描述三种情感控制方式
- ⚙️ **高级参数**: 提供采样参数调整
- 📊 **分割预览**: 文本分段预览功能

## 配置文件说明

| 文件 | 用途 |
|------|------|
| `runtime.txt` | 定义Python版本 (3.10.13) |
| `requirements.txt` | 项目依赖 |
| `koyeb.yml` | Koyeb构建配置 |
| `.koyeb-deploy.yaml` | GPU部署配置 |
| `.gitignore` | Git忽略配置 |

## 部署文档

- [DEPLOYMENT.md](DEPLOYMENT.md) - 详细部署指南
- [KOYEB_QUICK_START.md](KOYEB_QUICK_START.md) - 快速部署指南（中文）
- [DEPLOY_SUMMARY.md](DEPLOY_SUMMARY.md) - 部署总结
- [KOYEB_DEPLOY_CHECKLIST.md](KOYEB_DEPLOY_CHECKLIST.md) - 完整检查清单
- [PRE_DEPLOYMENT_CHECKLIST.txt](PRE_DEPLOYMENT_CHECKLIST.txt) - 部署前核实清单

## 依赖

所有依赖列在 `requirements.txt` 中，包括：
- `gradio` - Web UI框架
- `transformers` - Transformer模型
- `librosa` - 音频处理
- `spaces` - Hugging Face Spaces集成
- 以及其他音频和深度学习库

## 环境变量

部署时建议设置以下环境变量：

```
GRADIO_SHARE=false
HF_HOME=/workspace/.huggingface
TRANSFORMERS_CACHE=/workspace/.cache/transformers
```

## 支持

- [Koyeb文档](https://koyeb.com/docs)
- [IndexTTS2项目](https://github.com/InternLM/IndexTTS2)
- [Gradio文档](https://www.gradio.app)