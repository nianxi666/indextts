# Koyeb部署清单

## ✅ 已完成的配置

### 1. Python版本定义
- [x] `runtime.txt` - 定义Python 3.10.13
  - 位置：`/runtime.txt`
  - 内容：`python-3.10.13`

### 2. 依赖包配置
- [x] `requirements.txt` - 完整的项目依赖列表
  - 包含所有来自 `1.txt` 的依赖
  - 所有依赖都有版本号指定
  - 支持平台特定的依赖（Darwin vs 其他平台）

### 3. Koyeb构建配置
- [x] `koyeb.yml` - Koyeb构建和运行配置
  - 指定Python版本：3.10.13
  - 指定requirements文件
  - 配置运行命令：`python webui.py --host 0.0.0.0 --port $PORT`
  - 配置环境变量

### 4. GPU部署配置
- [x] `.koyeb-deploy.yaml` - GPU部署配置（A4000）
  - GPU类型：NVIDIA A4000
  - CPU：4核
  - 内存：16GB
  - 指定分支：`koyeb-deploy-gpu-a4000-github-define-python`

### 5. Git配置
- [x] `.gitignore` - Git忽略文件
  - 排除__pycache__和.pyc文件
  - 排除虚拟环境
  - 排除IDE配置
  - 排除模型检查点（大文件）
  - 排除缓存和日志

### 6. 文档
- [x] `DEPLOYMENT.md` - 详细部署指南
- [x] `KOYEB_DEPLOY_CHECKLIST.md` - 此检查清单

## 📋 部署前验证

在提交到Koyeb之前，请验证以下几点：

### 本地验证
- [ ] 运行 `python webui.py` 本地测试
- [ ] 确保所有依赖可以正常安装
- [ ] 验证模型下载功能

### 代码验证
- [ ] 所有文件已添加到Git
- [ ] 当前分支是 `koyeb-deploy-gpu-a4000-github-define-python`
- [ ] 没有未提交的关键更改

### 配置验证
- [ ] `runtime.txt` 包含 `python-3.10.13`
- [ ] `requirements.txt` 包含所有必需的依赖
- [ ] `koyeb.yml` 的运行命令正确
- [ ] `.koyeb-deploy.yaml` 指定了A4000 GPU

## 🚀 部署步骤

### 1. 使用Web UI部署（推荐）
```
1. 访问 https://app.koyeb.com
2. 使用您的账户登录
3. 创建新服务（Create Service）
4. 选择GitHub仓库
5. 选择分支：koyeb-deploy-gpu-a4000-github-define-python
6. 构建器：Python Buildpack
7. Python版本：3.10.13
8. 运行命令：python webui.py --host 0.0.0.0 --port $PORT
9. 资源配置：
   - GPU：NVIDIA A4000
   - CPU：4核
   - 内存：16GB
10. 环境变量：
    - GRADIO_SHARE=false
    - HF_HOME=/workspace/.huggingface
    - TRANSFORMERS_CACHE=/workspace/.cache/transformers
11. 点击Deploy
```

### 2. 使用CLI部署
```bash
export KOYEB_API_TOKEN="rocrorea70dhiis0zw0u68j35xve4ljjpt6ytw2sz7ixbr8y70ox7dpgqj497h28"

koyeb apps create indextts-webui \
  --git https://github.com/YOUR_USERNAME/YOUR_REPO \
  --git-branch koyeb-deploy-gpu-a4000-github-define-python \
  --builder buildpack \
  --buildpack-lang python \
  --buildpack-python-version 3.10.13 \
  --port 7860 \
  --instance-type gpu-a4000 \
  --min-scale 1 \
  --max-scale 1
```

## 📊 部署配置总结

| 项目 | 值 |
|------|-----|
| **分支** | `koyeb-deploy-gpu-a4000-github-define-python` |
| **Python版本** | 3.10.13 |
| **GPU** | NVIDIA A4000 |
| **CPU** | 4核 |
| **内存** | 16GB |
| **入口点** | `webui.py` |
| **主机** | 0.0.0.0 |
| **端口** | 7860（Gradio默认） |
| **运行命令** | `python webui.py --host 0.0.0.0 --port $PORT` |

## 🔧 环境变量

| 变量 | 值 | 说明 |
|------|-----|------|
| `GRADIO_SHARE` | false | 禁用Gradio公共分享（使用Koyeb URL） |
| `HF_HOME` | /workspace/.huggingface | Hugging Face缓存目录 |
| `TRANSFORMERS_CACHE` | /workspace/.cache/transformers | Transformers模型缓存 |

## ⏱️ 首次启动预期时间

- **构建时间**：10-20分钟（安装依赖）
- **模型下载**：5-15分钟（首次）
- **启动时间**：2-5分钟（初始化）
- **总计**：约20-40分钟

## 📝 注意事项

1. **首次启动较慢**：由于需要下载模型检查点，首次启动会比较慢
2. **GPU成本**：A4000是付费GPU，确保了解Koyeb的计费模式
3. **模型缓存**：模型会被缓存，后续启动会更快
4. **自动更新**：每次推送代码到此分支时会自动重新部署
5. **存储限制**：检查Koyeb存储配额，大型模型可能需要较多空间

## 🆘 故障排除

### 部署失败
- 检查构建日志：查看具体错误信息
- 验证依赖兼容性：确保所有依赖可以在Python 3.10.13上安装
- 检查网络：确保可以访问Hugging Face和PyPI

### 启动失败
- 查看运行日志：了解具体错误
- 检查端口：确保端口$PORT可用
- 验证GPU：确保A4000 GPU可用

### 模型下载失败
- 检查网络连接
- 验证Hugging Face访问权限
- 检查磁盘空间

## 📞 支持

- **Koyeb文档**：https://koyeb.com/docs
- **Koyeb支持**：https://koyeb.com/support
- **IndexTTS2**：https://github.com/InternLM/IndexTTS2

---

准备就绪！所有配置已完成，项目可以部署到Koyeb。
