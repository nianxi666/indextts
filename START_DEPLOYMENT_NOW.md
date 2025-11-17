# 🚀 现在就开始部署！ - Koyeb GPU H100

**重要**: 以下是实际的部署步骤，不再是只是脚本和文档。

---

## ⚡ 最快部署 (5分钟)

### 选项A: 一行命令部署 (最简单)

```bash
#!/bin/bash

# 1. 设置API密钥
export KOYEB_API_KEY="d5yqxgmxn08waujluulb2iczhsfi4kic1lfob7rs1skim4h2jajyxkiospyuxjex"

# 2. 设置Git仓库 (替换为您自己的仓库)
export GIT_REPO="https://github.com/your-org/indextts"

# 3. 执行部署 (方式1: 使用bash脚本)
bash koyeb-deploy.sh

# 或 (方式2: 使用curl)
curl -X POST https://app.koyeb.com/v1/deployments \
  -H "Authorization: Bearer $KOYEB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "displayName": "indextts-gpu-h100",
    "name": "indextts-gpu-h100",
    "instance": {"type": "gpu-h100"},
    "deployment": {
      "containerPort": 7860,
      "docker": {
        "command": ["python", "webui.py", "--host", "0.0.0.0", "--port", "7860"],
        "dockerfile": "Dockerfile"
      },
      "env": [
        {"key": "GRADIO_SERVER_NAME", "value": "0.0.0.0"},
        {"key": "GRADIO_SERVER_PORT", "value": "7860"}
      ],
      "resources": {"memory": "16Gi", "cpu": "8"},
      "ports": [{"port": 7860, "protocol": "http"}]
    },
    "git": {
      "branch": "main",
      "repository": "'$GIT_REPO'"
    }
  }'
```

### 选项B: 使用交互式脚本

```bash
# 最简单 - 按照提示输入信息
bash koyeb-deploy.sh

# 脚本会:
# 1. 检查依赖
# 2. 要求输入API密钥和仓库URL
# 3. 验证配置
# 4. 执行部署
# 5. 显示部署ID和状态URL
```

### 选项C: 使用Python脚本 (推荐 - 功能最完整)

```bash
# 1. 安装依赖
pip install requests

# 2. 执行部署 (替换为您自己的Git仓库)
export KOYEB_API_KEY="d5yqxgmxn08waujluulb2iczhsfi4kic1lfob7rs1skim4h2jajyxkiospyuxjex"

python3 deploy_koyeb_gpu_h100.py deploy \
  --git-repo https://github.com/your-org/indextts \
  --git-branch main \
  --wait

# --wait 表示: 等待部署完成，实时显示状态
```

---

## 📋 准备工作 (重要!)

### 1. Git仓库准备

确保您的GitHub仓库包含以下文件:

✅ **必需文件**:
- `Dockerfile` - 容器定义
- `webui.py` - 主应用
- `1.txt` - Python依赖列表
- `.gitignore` - Git忽略配置

✅ **仓库设置**:
- 仓库必须是 **PUBLIC** (公开)
- 或者使用SSH密钥认证

### 2. Dockerfile验证

```bash
# 本地测试构建
docker build -t indextts:test .

# 或本地运行
docker-compose up
```

### 3. API密钥

您的API密钥:
```
d5yqxgmxn08waujluulb2iczhsfi4kic1lfob7rs1skim4h2jajyxkiospyuxjex
```

保存在环境变量中:
```bash
export KOYEB_API_KEY="d5yqxgmxn08waujluulb2iczhsfi4kic1lfob7rs1skim4h2jajyxkiospyuxjex"

# 验证
echo $KOYEB_API_KEY
```

---

## 🔄 部署流程

### 步骤1: 部署

```bash
# 执行部署命令 (选择上面任一方式)
# 这会返回一个部署ID，例如: abc123xyz
```

### 步骤2: 获取部署ID

从部署响应中复制部署ID:
```json
{
  "id": "abc123xyz",  // <-- 这是您需要的ID
  "displayName": "indextts-gpu-h100",
  "status": "pending"
}
```

### 步骤3: 监控部署

```bash
# Python方式
python3 deploy_koyeb_gpu_h100.py status abc123xyz

# curl方式
curl https://app.koyeb.com/v1/deployments/abc123xyz \
  -H "Authorization: Bearer $KOYEB_API_KEY" | jq .

# Node.js方式
node deploy-koyeb-gpu-h100.js status abc123xyz
```

### 步骤4: 等待完成

监控状态直到看到:
```json
{
  "status": "active",
  "url": "https://indextts-gpu-h100.koyeb.app"
}
```

### 步骤5: 访问应用

打开浏览器访问返回的URL，应该看到Gradio WebUI！

---

## 📊 部署状态说明

| 状态 | 含义 | 预期时间 |
|-----|------|---------|
| `pending` | 正在初始化 | 1-2分钟 |
| `running` | 容器构建中 | 5-10分钟 |
| `active` | ✅ 部署完成 | 应用可访问 |
| `error` | ❌ 部署失败 | 查看日志 |

---

## 🔍 查看部署信息

### 列出所有部署

```bash
# Python
python3 deploy_koyeb_gpu_h100.py list

# curl
curl https://app.koyeb.com/v1/deployments \
  -H "Authorization: Bearer $KOYEB_API_KEY"

# Node.js
node deploy-koyeb-gpu-h100.js list
```

### 查看部署日志

```bash
# curl
curl https://app.koyeb.com/v1/deployments/<deployment-id>/logs \
  -H "Authorization: Bearer $KOYEB_API_KEY"
```

### 删除部署

```bash
# Python
python3 deploy_koyeb_gpu_h100.py delete <deployment-id>

# curl
curl -X DELETE https://app.koyeb.com/v1/deployments/<deployment-id> \
  -H "Authorization: Bearer $KOYEB_API_KEY"

# Node.js (无删除功能)
```

---

## 🛠️ 完整部署命令参考

### Python脚本完整选项

```bash
python3 deploy_koyeb_gpu_h100.py deploy \
  --git-repo <仓库URL> \                    # Git仓库地址
  --git-branch <分支> \                     # Git分支 (默认: main)
  --name <名称> \                           # 部署名称 (默认: indextts-gpu-h100)
  --instance-type <类型> \                  # GPU类型 (默认: gpu-h100)
  --memory <大小> \                         # 内存 (默认: 16Gi)
  --cpu <核数> \                            # CPU核数 (默认: 8)
  --docker-image <镜像> \                   # Docker镜像 (如果不用Git)
  --wait                                    # 等待部署完成
```

### curl完整示例

```bash
curl -X POST https://app.koyeb.com/v1/deployments \
  -H "Authorization: Bearer $KOYEB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "displayName": "indextts-gpu-h100",
    "name": "indextts-gpu-h100",
    "instance": {
      "type": "gpu-h100"
    },
    "deployment": {
      "containerPort": 7860,
      "docker": {
        "command": ["python", "webui.py", "--host", "0.0.0.0", "--port", "7860"],
        "dockerfile": "Dockerfile",
        "entrypoint": []
      },
      "env": [
        {
          "key": "GRADIO_SERVER_NAME",
          "value": "0.0.0.0"
        },
        {
          "key": "GRADIO_SERVER_PORT",
          "value": "7860"
        }
      ],
      "resources": {
        "memory": "16Gi",
        "cpu": "8"
      },
      "ports": [
        {
          "port": 7860,
          "protocol": "http"
        }
      ]
    },
    "git": {
      "branch": "main",
      "repository": "https://github.com/your-org/indextts"
    }
  }'
```

---

## 💰 成本考虑

### H100 GPU成本估算

| 使用方式 | 每月成本 | 备注 |
|---------|---------|------|
| 24/7运行 | ~$800-1000 | 连续运行 |
| 工作时间 (8h/day) | ~$300-400 | 一天8小时 |
| 按需测试 (2h/day) | ~$100-150 | 每天2小时 |

### 成本控制建议

✅ **做**:
- 完成测试后立即删除部署
- 监控实际使用时间
- 必要时使用更小的GPU实例
- 设置使用提醒

❌ **不要做**:
- 让部署长期运行而忘记删除
- 多个不必要的并行部署
- 在测试阶段使用H100

---

## ❓ 常见问题

### Q1: 我应该先做什么？

**A**: 按照以下顺序:
1. 准备GitHub仓库（确保公开）
2. 本地测试Docker构建
3. 设置API密钥环境变量
4. 执行部署命令
5. 监控部署状态

### Q2: 部署失败了怎么办？

**A**: 检查:
1. Git仓库是否公开
2. Dockerfile是否有效
3. 所有依赖是否在1.txt中
4. webui.py是否能本地运行
5. 查看部署日志

### Q3: 部署卡在pending状态怎么办？

**A**: 这是正常的! 容器构建需要时间:
- 首次部署: 5-10分钟
- 后续部署: 2-5分钟
- 使用 `--wait` 标志自动监控

### Q4: 怎么才能知道部署成功了？

**A**: 查看状态:
```bash
python3 deploy_koyeb_gpu_h100.py status <deployment-id>
```
当状态变为 `active` 时，部署成功！

### Q5: 如何更新已部署的应用？

**A**: 
1. 推送更新到Git仓库
2. 删除旧部署
3. 重新部署新版本

或者自动化:
```bash
# 在CI/CD中自动删除和重新部署
python3 deploy_koyeb_gpu_h100.py delete <deployment-id>
python3 deploy_koyeb_gpu_h100.py deploy --git-repo ... --wait
```

---

## 📞 需要帮助？

### 查看文档
1. [QUICK_START_DEPLOY.md](QUICK_START_DEPLOY.md) - 快速开始
2. [KOYEB_DEPLOYMENT_GUIDE.md](KOYEB_DEPLOYMENT_GUIDE.md) - 完整指南
3. [koyeb-api-examples.md](koyeb-api-examples.md) - API示例
4. [ACTUAL_DEPLOYMENT_EXAMPLE.md](ACTUAL_DEPLOYMENT_EXAMPLE.md) - 实际部署示例

### 官方资源
- [Koyeb文档](https://www.koyeb.com/docs)
- [Koyeb API文档](https://www.koyeb.com/docs/api)
- [Koyeb支持](https://www.koyeb.com/support)

### 检查脚本日志
```bash
# 启用详细日志
python3 -u deploy_koyeb_gpu_h100.py deploy \
  --git-repo https://github.com/your-org/indextts \
  --wait 2>&1 | tee deployment.log

# 查看日志
cat deployment.log
```

---

## ✅ 实际部署检查清单

准备好了吗？检查以下项目:

- [ ] Git仓库已准备并公开
- [ ] Dockerfile已验证
- [ ] webui.py已测试
- [ ] API密钥已设置: `d5yqxgmxn08waujluulb2iczhsfi4kic1lfob7rs1skim4h2jajyxkiospyuxjex`
- [ ] 依赖文件 (1.txt) 已完成
- [ ] 理解了H100 GPU成本
- [ ] 选择了部署方式 (Python/curl/bash)
- [ ] 准备好了部署后监控

---

## 🚀 现在就部署！

### 最快方式 (一行命令)

```bash
# 设置环境变量
export KOYEB_API_KEY="d5yqxgmxn08waujluulb2iczhsfi4kic1lfob7rs1skim4h2jajyxkiospyuxjex"

# 部署 (替换为您的Git仓库)
python3 deploy_koyeb_gpu_h100.py deploy \
  --git-repo https://github.com/your-org/indextts \
  --wait

# 部署完成！访问返回的URL
```

### 交互式方式

```bash
# 按照提示操作
bash koyeb-deploy.sh
```

---

## 📝 部署后记录

保存以下信息以便后续使用:

```
部署日期: ______________
部署ID: ______________
应用URL: ______________
Git仓库: ______________
API密钥: d5yqxgmxn08waujluulb2iczhsfi4kic1lfob7rs1skim4h2jajyxkiospyuxjex
备注: ______________
```

---

**准备好了吗？现在就开始您的第一次H100 GPU部署吧！🚀**

*预计完成时间: 10-15分钟（包括容器构建）*

