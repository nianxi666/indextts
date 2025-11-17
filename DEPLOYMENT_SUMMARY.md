# Koyeb GPU H100 部署 - 完整总结

## 📋 概览

本项目实现了完整的Koyeb容器部署解决方案，支持使用以下方式部署IndexTTS应用到带NVIDIA H100 GPU的容器：

- ✅ **curl** - 直接调用Koyeb API
- ✅ **JavaScript/Node.js** - 完整的部署管理工具
- ✅ **Python** - 高级部署脚本，支持状态监控
- ✅ **Docker** - 本地开发和容器化运行

---

## 📁 项目文件结构

### 部署脚本

| 文件 | 类型 | 用途 | 执行 |
|-----|------|------|------|
| `deploy-koyeb-gpu-h100.sh` | Bash | curl基础部署 | `bash deploy-koyeb-gpu-h100.sh` |
| `deploy-koyeb-gpu-h100.js` | Node.js | JavaScript部署工具 | `node deploy-koyeb-gpu-h100.js` |
| `deploy_koyeb_gpu_h100.py` | Python | Python部署工具（推荐） | `python3 deploy_koyeb_gpu_h100.py` |

### Docker相关

| 文件 | 说明 |
|-----|------|
| `Dockerfile` | 基于CUDA 12.2的容器镜像定义 |
| `docker-compose.yml` | Docker Compose配置，支持GPU |

### 配置和文档

| 文件 | 说明 |
|-----|------|
| `.env.example` | 环境变量示例配置 |
| `.gitignore` | Git忽略配置（保护敏感信息） |
| `package.json` | Node.js项目配置 |
| `README.md` | 项目主文档 |
| `QUICK_START_DEPLOY.md` | 5分钟快速启动指南 |
| `KOYEB_DEPLOYMENT_GUIDE.md` | 完整部署指南（70+章节） |
| `koyeb-api-examples.md` | API调用完整示例 |
| `DEPLOYMENT_SUMMARY.md` | 本文件 |

---

## 🚀 快速开始（3步）

### 步骤1: 选择部署方式

#### 方式A: curl (最简单 - 1行命令)
```bash
bash deploy-koyeb-gpu-h100.sh
```

#### 方式B: Python (推荐 - 功能最完整)
```bash
pip install requests
python3 deploy_koyeb_gpu_h100.py deploy \
  --git-repo https://github.com/your-org/indextts \
  --wait  # 等待部署完成
```

#### 方式C: Node.js
```bash
node deploy-koyeb-gpu-h100.js
```

### 步骤2: 获取部署ID

从上述命令的响应中获取 `id` 字段。

### 步骤3: 监控部署

```bash
# Python
python3 deploy_koyeb_gpu_h100.py status <deployment-id>

# Node.js
node deploy-koyeb-gpu-h100.js status <deployment-id>

# curl
curl https://app.koyeb.com/v1/deployments/<deployment-id> \
  -H "Authorization: Bearer $KOYEB_API_KEY"
```

---

## 🎯 部署配置说明

### 核心配置
- **GPU**: NVIDIA H100 (80GB VRAM)
- **内存**: 16Gi
- **CPU**: 8核
- **端口**: 7860 (Gradio默认)
- **基础镜像**: nvidia/cuda:12.2.2-devel-ubuntu22.04

### 可自定义参数

| 参数 | 默认值 | 说明 |
|-----|--------|------|
| `deployment_name` | indextts-gpu-h100 | 应用部署名称 |
| `instance_type` | gpu-h100 | GPU实例类型 |
| `memory` | 16Gi | 系统内存 |
| `cpu` | 8 | CPU核心数 |
| `git_branch` | main | Git分支 |

### GPU实例类型选项

| 类型 | GPU | VRAM | 成本 | 用途 |
|-----|-----|------|------|------|
| `gpu-h100` | H100 | 80GB | 💸💸💸 | ⭐ 高性能推理 |
| `gpu-a100` | A100 | 40GB | 💸💸 | 中等性能 |
| `gpu-t4` | T4 | 16GB | 💸 | 低功耗 |
| `cpu` | CPU | 可配 | 💸 | 开发测试 |

---

## 📊 部署工具对比

| 功能 | curl脚本 | Node.js | Python |
|-----|---------|--------|--------|
| 部署 | ✅ | ✅ | ✅ |
| 查看状态 | ✅ | ✅ | ✅ |
| 列出部署 | ❌ | ✅ | ✅ |
| 删除部署 | ❌ | ❌ | ✅ |
| 等待监控 | ❌ | ❌ | ✅ |
| 错误处理 | 基础 | 中等 | 完整 |
| 易用性 | ★★★ | ★★ | ★★★ |
| 功能完整 | ★ | ★★★ | ★★★★ |

**推荐**: 使用Python脚本以获得最完整的功能。

---

## 🔐 安全配置

### API密钥管理

❌ **不要做**:
```bash
# 在脚本中硬编码密钥
curl ... -H "Authorization: Bearer d5yqxgmxn08waujluulb2iczhsfi4kic1lfob7rs1skim4h2jajyxkiospyuxjex"
```

✅ **推荐做法**:
```bash
# 使用环境变量
export KOYEB_API_KEY="d5yqxgmxn08waujluulb2iczhsfi4kic1lfob7rs1skim4h2jajyxkiospyuxjex"

# 或使用.env文件
cp .env.example .env
# 编辑.env文件添加密钥
```

### 仓库安全

- ✅ `.gitignore` 已配置，保护 `.env` 和敏感文件
- ✅ 不提交模型文件和缓存到Git
- ✅ 使用私有仓库存储敏感配置

---

## 📖 详细文档导航

### 快速查找

1. **立即开始** → [QUICK_START_DEPLOY.md](QUICK_START_DEPLOY.md)
   - 5分钟快速部署
   - 常见问题解答
   - 示例命令

2. **深入学习** → [KOYEB_DEPLOYMENT_GUIDE.md](KOYEB_DEPLOYMENT_GUIDE.md)
   - 完整配置说明
   - 部署参数详解
   - 监控和维护
   - 故障排除指南

3. **API参考** → [koyeb-api-examples.md](koyeb-api-examples.md)
   - curl完整示例
   - JavaScript示例
   - Python示例
   - 高级配置
   - API端点文档

4. **项目文档** → [README.md](README.md)
   - 项目概览
   - 快速命令
   - 常用操作

---

## 🛠️ 环境要求

### 对于curl脚本
- Linux/Mac/Windows (Git Bash)
- curl (通常预装)

### 对于Node.js脚本
- Node.js >= 14.0.0
- npm 或 yarn

### 对于Python脚本
- Python >= 3.8
- requests 库 (`pip install requests`)

### 对于Docker
- Docker >= 20.0
- Docker Compose >= 1.29 (可选)
- NVIDIA Docker Runtime (可选，本地GPU测试)

---

## 📝 常见命令速查

### 部署应用

```bash
# Python (推荐)
python3 deploy_koyeb_gpu_h100.py deploy \
  --git-repo https://github.com/your-org/indextts \
  --git-branch main \
  --wait

# Node.js
node deploy-koyeb-gpu-h100.js

# Bash
bash deploy-koyeb-gpu-h100.sh
```

### 查看状态

```bash
# Python
python3 deploy_koyeb_gpu_h100.py status <deployment-id>

# Node.js
node deploy-koyeb-gpu-h100.js status <deployment-id>

# curl
curl https://app.koyeb.com/v1/deployments/<deployment-id> \
  -H "Authorization: Bearer $KOYEB_API_KEY"
```

### 列出所有部署

```bash
# Python
python3 deploy_koyeb_gpu_h100.py list

# Node.js
node deploy-koyeb-gpu-h100.js list

# curl
curl https://app.koyeb.com/v1/deployments \
  -H "Authorization: Bearer $KOYEB_API_KEY"
```

### 删除部署

```bash
# Python
python3 deploy_koyeb_gpu_h100.py delete <deployment-id>

# curl
curl -X DELETE https://app.koyeb.com/v1/deployments/<deployment-id> \
  -H "Authorization: Bearer $KOYEB_API_KEY"
```

### 本地Docker运行

```bash
# 构建镜像
docker build -t indextts:latest .

# 使用Docker Compose运行
docker-compose up -d

# 查看日志
docker-compose logs -f indextts

# 停止容器
docker-compose down
```

---

## 🔍 监控和调试

### 查看部署日志

```bash
curl https://app.koyeb.com/v1/deployments/<deployment-id>/logs \
  -H "Authorization: Bearer $KOYEB_API_KEY" | jq .
```

### 检查部署健康状态

应用启动后会自动通过健康检查端点：
```
GET http://<deployment-url>/health
```

### 常见问题排查

| 问题 | 检查项 |
|-----|--------|
| 部署失败 | 查看日志，验证Dockerfile和依赖 |
| 401错误 | 检查API密钥是否正确 |
| 400错误 | 验证JSON配置格式 |
| GPU不可用 | 确认账户有GPU配额 |
| 应用无法启动 | 查看应用日志和启动命令 |

---

## 💡 最佳实践

### 1. 使用环境变量
```bash
export KOYEB_API_KEY="..."
export GIT_REPO="..."
```

### 2. 测试配置
```bash
# 使用Python脚本验证配置
python3 deploy_koyeb_gpu_h100.py deploy \
  --git-repo ... \
  --wait  # 等待完成，便于调试
```

### 3. 监控成本
- 定期检查运行时间
- 不使用时删除部署
- 根据需求调整资源

### 4. 备份和恢复
- 保存部署配置
- 记录部署ID
- 维护配置版本历史

### 5. 安全性
- 使用环境变量存储密钥
- 定期轮换API密钥
- 限制仓库访问权限

---

## 🤝 支持和反馈

### 获取帮助
1. 查看 [快速启动指南](QUICK_START_DEPLOY.md)
2. 查看 [完整部署指南](KOYEB_DEPLOYMENT_GUIDE.md)
3. 查看 [API示例文档](koyeb-api-examples.md)
4. 访问 [Koyeb官方文档](https://www.koyeb.com/docs)

### 报告问题
- 检查应用日志
- 验证配置参数
- 查看故障排除指南

### Koyeb官方支持
- [Koyeb支持中心](https://www.koyeb.com/support)
- [Koyeb社区](https://community.koyeb.com)

---

## 📚 相关资源

### 官方文档
- [Koyeb文档](https://www.koyeb.com/docs)
- [Koyeb API文档](https://www.koyeb.com/docs/api)
- [NVIDIA CUDA文档](https://docs.nvidia.com/cuda/)

### 项目参考
- [IndexTTS项目](https://github.com/your-org/indextts)
- [Gradio文档](https://gradio.app)
- [Docker文档](https://docs.docker.com)

---

## 📄 文件清单

项目包含以下部署相关文件（共12个新增文件）：

```
部署脚本 (3个):
├── deploy-koyeb-gpu-h100.sh       (2.8K)
├── deploy-koyeb-gpu-h100.js       (8.3K)
└── deploy_koyeb_gpu_h100.py       (14K)

Docker配置 (2个):
├── Dockerfile                      (1.3K)
└── docker-compose.yml              (928B)

配置文件 (2个):
├── .env.example                    (667B)
└── .gitignore                      (596B)

项目配置 (1个):
└── package.json                    (787B)

文档 (4个):
├── QUICK_START_DEPLOY.md           (7.1K)
├── KOYEB_DEPLOYMENT_GUIDE.md       (6.9K)
├── koyeb-api-examples.md           (14K)
└── DEPLOYMENT_SUMMARY.md           (本文件)

修改:
└── README.md                       (已更新)

总计: 57KB+ 的文档和脚本
```

---

## ✅ 部署检查清单

在部署前请检查：

- [ ] API密钥已获取
- [ ] Git仓库已准备（包含Dockerfile和webui.py）
- [ ] 环境变量已配置
- [ ] 选择了合适的部署工具
- [ ] 理解了GPU成本
- [ ] 查看了快速启动指南

---

## 🎉 下一步

1. **立即开始**: 按照 [QUICK_START_DEPLOY.md](QUICK_START_DEPLOY.md) 部署
2. **深入学习**: 阅读 [KOYEB_DEPLOYMENT_GUIDE.md](KOYEB_DEPLOYMENT_GUIDE.md)
3. **探索API**: 查看 [koyeb-api-examples.md](koyeb-api-examples.md)
4. **优化部署**: 根据需求调整资源和配置

---

**祝部署顺利！🚀**

*最后更新: 2024年*
