# IndexTTS - Koyeb GPU H100 Deployment

一个IndexTTS WebUI，支持使用Koyeb官方API部署到带H100 GPU的容器。

## 🚀 快速开始

### 部署到Koyeb（H100 GPU）

我们提供了三种部署方式，选择最适合您的方式：

#### 方式1️⃣: 使用curl (最简单)

```bash
bash deploy-koyeb-gpu-h100.sh
```

详见: [deploy-koyeb-gpu-h100.sh](deploy-koyeb-gpu-h100.sh)

#### 方式2️⃣: 使用Node.js

```bash
node deploy-koyeb-gpu-h100.js
```

详见: [deploy-koyeb-gpu-h100.js](deploy-koyeb-gpu-h100.js)

#### 方式3️⃣: 使用Python

```bash
pip install requests
python3 deploy_koyeb_gpu_h100.py deploy --git-repo https://github.com/your-org/indextts
```

详见: [deploy_koyeb_gpu_h100.py](deploy_koyeb_gpu_h100.py)

## 📚 文档

- **[快速启动指南](QUICK_START_DEPLOY.md)** - 5分钟快速部署
- **[完整部署指南](KOYEB_DEPLOYMENT_GUIDE.md)** - 详细的部署和配置说明
- **[API示例](koyeb-api-examples.md)** - curl、JavaScript、Python API调用示例

## 📋 文件说明

| 文件 | 说明 |
|-----|------|
| `deploy-koyeb-gpu-h100.sh` | Bash脚本部署工具 |
| `deploy-koyeb-gpu-h100.js` | Node.js部署工具 |
| `deploy_koyeb_gpu_h100.py` | Python部署工具 |
| `Dockerfile` | Docker容器镜像定义 |
| `docker-compose.yml` | Docker Compose配置 |
| `package.json` | Node.js项目配置 |
| `.env.example` | 环境变量示例 |
| `KOYEB_DEPLOYMENT_GUIDE.md` | 完整部署指南 |
| `QUICK_START_DEPLOY.md` | 快速启动指南 |
| `koyeb-api-examples.md` | API调用示例 |

## 🔧 环境变量配置

复制 `.env.example` 到 `.env` 并配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```bash
# Koyeb API配置
KOYEB_API_KEY=d5yqxgmxn08waujluulb2iczhsfi4kic1lfob7rs1skim4h2jajyxkiospyuxjex

# 部署配置
DEPLOYMENT_NAME=indextts-gpu-h100
INSTANCE_TYPE=gpu-h100
CONTAINER_PORT=7860
MEMORY=16Gi
CPU=8

# 其他配置...
```

## 🎮 实例类型

| 实例类型 | GPU | VRAM | 推荐用途 |
|---------|-----|------|---------|
| `gpu-h100` | NVIDIA H100 | 80GB | ⭐ 高性能推理（推荐） |
| `gpu-a100` | NVIDIA A100 | 40GB | 中等性能任务 |
| `gpu-t4` | NVIDIA T4 | 16GB | 通用GPU计算 |
| `cpu` | CPU只 | 可配置 | 开发/测试 |

## 📊 部署配置

默认配置：
- **GPU**: NVIDIA H100
- **内存**: 16Gi
- **CPU**: 8核
- **端口**: 7860

可根据需要在部署脚本中修改。

## 🔍 常用命令

### 使用Python脚本

```bash
# 部署
python3 deploy_koyeb_gpu_h100.py deploy \
  --git-repo https://github.com/your-org/indextts \
  --git-branch main

# 查看部署状态
python3 deploy_koyeb_gpu_h100.py status <deployment-id>

# 列出所有部署
python3 deploy_koyeb_gpu_h100.py list

# 删除部署
python3 deploy_koyeb_gpu_h100.py delete <deployment-id>

# 等待部署完成
python3 deploy_koyeb_gpu_h100.py deploy \
  --git-repo https://github.com/your-org/indextts \
  --wait
```

### 使用curl

```bash
# 部署
bash deploy-koyeb-gpu-h100.sh

# 检查状态
bash deploy-koyeb-gpu-h100.sh status <deployment-id>
```

### 使用Node.js

```bash
# 部署
node deploy-koyeb-gpu-h100.js

# 查看状态
node deploy-koyeb-gpu-h100.js status <deployment-id>

# 列出部署
node deploy-koyeb-gpu-h100.js list
```

## 🐳 本地Docker运行

```bash
# 构建镜像
docker build -t indextts:latest .

# 使用docker-compose运行
docker-compose up -d

# 访问应用
# http://localhost:7860
```

## 📖 Koyeb官方文档

- [Koyeb文档](https://www.koyeb.com/docs)
- [Koyeb API文档](https://www.koyeb.com/docs/api)
- [Koyeb支持](https://www.koyeb.com/support)

## ⚠️ 重要提示

- ✅ 不要在代码中硬编码API密钥，使用环境变量
- ✅ 确保Git仓库包含 `Dockerfile` 和 `webui.py`
- ✅ 监控GPU使用成本
- ✅ 定期检查部署日志

## 🆘 获取帮助

1. 查看 [QUICK_START_DEPLOY.md](QUICK_START_DEPLOY.md) 快速开始
2. 查看 [KOYEB_DEPLOYMENT_GUIDE.md](KOYEB_DEPLOYMENT_GUIDE.md) 完整指南
3. 查看 [koyeb-api-examples.md](koyeb-api-examples.md) API示例
4. 访问 [Koyeb支持中心](https://www.koyeb.com/support)

## 📝 许可证

MIT License