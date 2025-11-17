# 实际部署示例 - Koyeb H100 GPU容器

本文档展示如何使用提供的API密钥和部署工具实际部署容器到Koyeb。

## 🔑 您的部署凭证

```
API密钥: d5yqxgmxn08waujluulb2iczhsfi4kic1lfob7rs1skim4h2jajyxkiospyuxjex
API端点: https://app.koyeb.com/v1
```

## 方式1️⃣: 使用Python脚本部署 (推荐)

### 步骤1: 设置环境

```bash
# 克隆仓库
git clone <your-repo> indextts-deployment
cd indextts-deployment

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install requests
```

### 步骤2: 配置部署参数

创建 `.env` 文件:

```bash
cat > .env << 'EOF'
KOYEB_API_KEY=d5yqxgmxn08waujluulb2iczhsfi4kic1lfob7rs1skim4h2jajyxkiospyuxjex
DEPLOYMENT_NAME=indextts-gpu-h100
INSTANCE_TYPE=gpu-h100
MEMORY=16Gi
CPU=8
GIT_REPO=https://github.com/your-org/indextts
GIT_BRANCH=main
EOF
```

### 步骤3: 执行部署

```bash
# 设置环境变量
export KOYEB_API_KEY=d5yqxgmxn08waujluulb2iczhsfi4kic1lfob7rs1skim4h2jajyxkiospyuxjex

# 部署并等待完成
python3 deploy_koyeb_gpu_h100.py deploy \
  --git-repo https://github.com/your-org/indextts \
  --git-branch main \
  --name indextts-gpu-h100 \
  --instance-type gpu-h100 \
  --memory 16Gi \
  --cpu 8 \
  --wait

# 或者简单形式
python3 deploy_koyeb_gpu_h100.py deploy \
  --git-repo https://github.com/your-org/indextts \
  --wait
```

### 步骤4: 监控部署

部署完成后，您会看到部署ID，使用它来查询状态:

```bash
# 查看状态
python3 deploy_koyeb_gpu_h100.py status <deployment-id>

# 列出所有部署
python3 deploy_koyeb_gpu_h100.py list

# 删除部署
python3 deploy_koyeb_gpu_h100.py delete <deployment-id>
```

---

## 方式2️⃣: 使用curl直接部署

### 一行命令部署

```bash
export API_KEY="d5yqxgmxn08waujluulb2iczhsfi4kic1lfob7rs1skim4h2jajyxkiospyuxjex"
export GIT_REPO="https://github.com/your-org/indextts"

curl -X POST https://app.koyeb.com/v1/deployments \
  -H "Authorization: Bearer $API_KEY" \
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
  }' | jq .
```

### 查看部署状态

```bash
DEPLOYMENT_ID="<从上面获取的ID>"

curl https://app.koyeb.com/v1/deployments/$DEPLOYMENT_ID \
  -H "Authorization: Bearer $API_KEY" | jq .
```

---

## 方式3️⃣: 使用Bash脚本部署

```bash
# 直接执行部署脚本
bash deploy-koyeb-gpu-h100.sh
```

---

## 方式4️⃣: 使用Node.js部署

```bash
# 确保安装了Node.js
node --version  # 需要 >= 14.0.0

# 部署
export KOYEB_API_KEY=d5yqxgmxn08waujluulb2iczhsfi4kic1lfob7rs1skim4h2jajyxkiospyuxjex
node deploy-koyeb-gpu-h100.js

# 查看状态
node deploy-koyeb-gpu-h100.js status <deployment-id>

# 列出所有
node deploy-koyeb-gpu-h100.js list
```

---

## 📋 Git仓库准备清单

确保您的GitHub仓库包含以下文件:

- [ ] `webui.py` - 主应用文件
- [ ] `Dockerfile` - 容器镜像定义
- [ ] `1.txt` - Python依赖文件
- [ ] `.gitignore` - Git忽略配置
- [ ] `README.md` - 项目说明

仓库必须是**公开的**或使用SSH密钥认证。

---

## 🔍 部署后验证

### 1. 检查部署状态

```bash
python3 deploy_koyeb_gpu_h100.py status <deployment-id>
```

期望输出:
```json
{
  "id": "...",
  "status": "active",
  "url": "https://indextts-gpu-h100.koyeb.app",
  ...
}
```

### 2. 访问应用

打开浏览器访问返回的 `url` 地址，应该看到Gradio WebUI界面。

### 3. 检查GPU是否正常工作

在WebUI中查看日志，应该看到类似:
```
GPU信息: NVIDIA H100
CUDA可用: True
```

---

## 🛠️ 故障排除

### 问题1: 401 错误

**原因**: API密钥无效

**解决**:
```bash
# 验证密钥格式
echo "d5yqxgmxn08waujluulb2iczhsfi4kic1lfob7rs1skim4h2jajyxkiospyuxjex" | wc -c
# 应该是80个字符

# 再次尝试
export KOYEB_API_KEY="d5yqxgmxn08waujluulb2iczhsfi4kic1lfob7rs1skim4h2jajyxkiospyuxjex"
python3 deploy_koyeb_gpu_h100.py deploy --git-repo ...
```

### 问题2: 400 错误

**原因**: 配置格式错误或Git仓库问题

**解决**:
- 验证Git仓库是公开的
- 检查Dockerfile是否有效
- 确保所有必需文件都在仓库中

### 问题3: 部署卡在 "pending" 状态

**原因**: 正在构建容器

**解决**:
- 等待5-10分钟，容器构建需要时间
- 查看部署日志:
```bash
curl https://app.koyeb.com/v1/deployments/<id>/logs \
  -H "Authorization: Bearer $KOYEB_API_KEY" | jq .
```

### 问题4: 应用无法启动

**原因**: 依赖或webui.py有问题

**解决**:
- 检查本地是否能运行: `python3 webui.py`
- 验证所有依赖都在 `1.txt` 中
- 查看完整的部署日志

---

## 💡 成本估算

H100 GPU成本（估算）:
- **$30-40 / 天** (连续运行)
- **$1-2 / 小时** (按需)

建议:
- 测试时使用较小的GPU实例
- 不使用时立即删除部署
- 监控实际使用时间和成本

---

## 📝 后续操作

### 部署后

1. **访问应用**
   - 打开WebUI URL
   - 测试TTS功能

2. **监控性能**
   - 检查GPU利用率
   - 监控内存使用
   - 查看应用日志

3. **更新应用**
   - 修改代码后提交到Git
   - 重新部署或更新部署

### 生产部署

1. **配置域名**
   - 设置自定义域名
   - 配置HTTPS

2. **设置监控告警**
   - 配置崩溃告警
   - 监控成本

3. **自动化更新**
   - CI/CD流程
   - 自动重新部署

---

## 🆘 获取帮助

1. **查看文档**
   - [QUICK_START_DEPLOY.md](QUICK_START_DEPLOY.md)
   - [KOYEB_DEPLOYMENT_GUIDE.md](KOYEB_DEPLOYMENT_GUIDE.md)
   - [koyeb-api-examples.md](koyeb-api-examples.md)

2. **检查脚本日志**
   ```bash
   python3 deploy_koyeb_gpu_h100.py deploy \
     --git-repo ... \
     --wait  # 等待完成，查看所有日志
   ```

3. **Koyeb官方支持**
   - [Koyeb文档](https://www.koyeb.com/docs)
   - [Koyeb支持](https://www.koyeb.com/support)

---

## ✅ 部署检查清单

部署前确保:

- [ ] API密钥已验证: `d5yqxgmxn08waujluulb2iczhsfi4kic1lfob7rs1skim4h2jajyxkiospyuxjex`
- [ ] Git仓库已准备并公开
- [ ] Dockerfile已验证
- [ ] webui.py已测试
- [ ] 依赖文件已完善
- [ ] 理解了成本含义
- [ ] 选择了合适的部署工具

---

**准备好了吗？现在就开始部署吧！🚀**

```bash
# 最简单的一行部署命令
export KOYEB_API_KEY=d5yqxgmxn08waujluulb2iczhsfi4kic1lfob7rs1skim4h2jajyxkiospyuxjex && \
python3 deploy_koyeb_gpu_h100.py deploy --git-repo https://github.com/your-org/indextts --wait
```
