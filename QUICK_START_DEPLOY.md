# 快速启动 - Koyeb GPU H100 部署

这个指南将帮您快速部署IndexTTS到Koyeb，使用H100 GPU。

## 🚀 5分钟快速部署

### 前置准备

1. **获取API密钥**: 访问 [Koyeb控制面板](https://app.koyeb.com)
2. **设置Git仓库**: 将IndexTTS推送到GitHub
3. **选择部署方式**: 下面提供3种方式，任选其一

---

## 方式1️⃣: 直接使用curl（最简单）

### 在Linux/Mac终端执行：

```bash
# 1. 设置变量
export API_KEY="d5yqxgmxn08waujluulb2iczhsfi4kic1lfob7rs1skim4h2jajyxkiospyuxjex"
export GIT_REPO="https://github.com/YOUR_USER/indextts"

# 2. 部署
curl -X POST https://app.koyeb.com/v1/deployments \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "displayName": "indextts-gpu-h100",
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
      "resources": {
        "memory": "16Gi",
        "cpu": "8"
      },
      "ports": [{"port": 7860, "protocol": "http"}]
    },
    "git": {
      "branch": "main",
      "repository": "'$GIT_REPO'"
    },
    "instance": {"type": "gpu-h100"},
    "name": "indextts-gpu-h100"
  }'
```

✅ **完成！** 复制返回的 `id` 字段，用于后续查询状态。

---

## 方式2️⃣: 使用Node.js脚本

### 在Linux/Mac/Windows执行：

```bash
# 1. 确保安装了Node.js (v14+)
node --version

# 2. 部署
node deploy-koyeb-gpu-h100.js

# 3. 查看部署状态
node deploy-koyeb-gpu-h100.js status <deployment-id>

# 4. 列出所有部署
node deploy-koyeb-gpu-h100.js list
```

---

## 方式3️⃣: 使用Python脚本

### 在Linux/Mac/Windows执行：

```bash
# 1. 确保安装了Python3 (3.8+) 和 requests
pip install requests

# 2. 部署（从Git仓库）
python3 deploy_koyeb_gpu_h100.py deploy \
  --git-repo https://github.com/YOUR_USER/indextts \
  --git-branch main

# 3. 或者从Docker镜像部署
python3 deploy_koyeb_gpu_h100.py deploy \
  --docker-image your-org/indextts:latest

# 4. 查看部署状态
python3 deploy_koyeb_gpu_h100.py status <deployment-id>

# 5. 等待部署完成并监控
python3 deploy_koyeb_gpu_h100.py deploy \
  --git-repo https://github.com/YOUR_USER/indextts \
  --wait

# 6. 列出所有部署
python3 deploy_koyeb_gpu_h100.py list

# 7. 删除部署
python3 deploy_koyeb_gpu_h100.py delete <deployment-id>
```

---

## 📋 部署参数说明

| 参数 | 说明 | 示例值 |
|-----|------|--------|
| `displayName` | 显示名称 | `indextts-gpu-h100` |
| `containerPort` | 容器端口 | `7860` |
| `memory` | 内存大小 | `16Gi` |
| `cpu` | CPU核心数 | `8` |
| `instance.type` | GPU类型 | `gpu-h100` (H100), `gpu-a100` (A100) |
| `repository` | Git仓库 | `https://github.com/user/repo` |
| `branch` | Git分支 | `main`, `master`, `dev` |

---

## ⚠️ 重要提示

### API密钥安全性
🔒 **不要在代码中硬编码API密钥！**

使用环境变量替代：

**Linux/Mac:**
```bash
export KOYEB_API_KEY="你的密钥"
# 然后使用变量
curl -H "Authorization: Bearer $KOYEB_API_KEY" ...
```

**Windows (PowerShell):**
```powershell
$env:KOYEB_API_KEY="你的密钥"
$key = $env:KOYEB_API_KEY
```

### Git仓库要求
- ✅ 必须包含 `Dockerfile`
- ✅ 必须包含 `webui.py`
- ✅ 必须包含 `1.txt` (依赖文件)
- ✅ 仓库必须是公开的（或使用SSH密钥）

### Docker镜像要求
- ✅ 镜像必须包含Python和依赖
- ✅ 必须暴露端口 7860
- ✅ 必须能够通过 `python webui.py` 启动

---

## 🔍 查看部署状态

### 使用curl：
```bash
API_KEY="你的密钥"
DEPLOYMENT_ID="从部署返回的ID"

curl https://app.koyeb.com/v1/deployments/$DEPLOYMENT_ID \
  -H "Authorization: Bearer $API_KEY"
```

### 使用Python脚本：
```bash
python3 deploy_koyeb_gpu_h100.py status <deployment-id>
```

### 响应示例：
```json
{
  "id": "abc123xyz",
  "displayName": "indextts-gpu-h100",
  "status": "active",
  "url": "https://indextts-gpu-h100.koyeb.app",
  "createdAt": "2024-01-01T12:00:00Z"
}
```

状态可能的值：
- `pending` - 等待中
- `active` - 已激活，可以使用
- `error` - 出错
- `inactive` - 已停用

---

## 🛑 停止和删除部署

### 使用curl：
```bash
API_KEY="你的密钥"
DEPLOYMENT_ID="部署ID"

curl -X DELETE https://app.koyeb.com/v1/deployments/$DEPLOYMENT_ID \
  -H "Authorization: Bearer $API_KEY"
```

### 使用Python脚本：
```bash
python3 deploy_koyeb_gpu_h100.py delete <deployment-id>
```

---

## 📊 监控和性能优化

### 查看应用日志：
```bash
curl https://app.koyeb.com/v1/deployments/<deployment-id>/logs \
  -H "Authorization: Bearer $API_KEY"
```

### 性能建议：
- 👍 **H100 GPU**: 高性能推理（推荐用于生产环境）
- 👍 **16Gi 内存**: 足以运行IndexTTS
- 👍 **8 CPU核心**: 平衡计算和成本
- 👍 **启用FP16**: 在webui.py中添加 `--fp16` 提高性能

### 成本控制：
- 监控GPU使用时间
- 在不使用时删除部署
- 考虑使用更小的实例进行开发/测试

---

## ❓ 常见问题

### Q1: 部署失败，显示401错误？
**A:** 检查API密钥是否正确
```bash
# 验证密钥
curl https://app.koyeb.com/v1/account \
  -H "Authorization: Bearer $API_KEY"
```

### Q2: 部署失败，显示400错误？
**A:** 检查JSON配置格式和必需字段
```bash
# 验证JSON格式
echo '你的JSON配置' | jq .
```

### Q3: 如何访问部署的应用？
**A:** 从部署状态响应的 `url` 字段获取
```bash
# 获取URL
python3 deploy_koyeb_gpu_h100.py status <deployment-id>

# 会返回 url 字段，例如:
# https://indextts-gpu-h100.koyeb.app
```

### Q4: GPU内存不足？
**A:** 增加内存和CPU资源
```bash
python3 deploy_koyeb_gpu_h100.py deploy \
  --memory 32Gi \
  --cpu 16
```

### Q5: 如何使用自己的Docker镜像？
**A:** 先推送镜像到Docker Hub，然后使用 `--docker-image`
```bash
python3 deploy_koyeb_gpu_h100.py deploy \
  --docker-image your-username/indextts:v1.0
```

---

## 🎯 下一步

1. **部署成功后**
   - 访问应用URL
   - 测试TTS功能
   - 检查GPU利用率

2. **优化和维护**
   - 监控日志和性能
   - 更新依赖
   - 定期备份配置

3. **生产部署**
   - 配置自定义域名
   - 设置监控告警
   - 实现自动化更新

---

## 📚 更多资源

- [Koyeb官方文档](https://www.koyeb.com/docs)
- [Koyeb API文档](https://www.koyeb.com/docs/api)
- [IndexTTS项目](https://github.com/your-org/indextts)
- [NVIDIA H100 文档](https://www.nvidia.com/en-us/data-center/h100/)
- [Gradio 文档](https://gradio.app)

---

## 🆘 获取帮助

遇到问题？

1. **查看部署日志**
   ```bash
   python3 deploy_koyeb_gpu_h100.py status <deployment-id>
   ```

2. **检查应用输出**
   - 查看Koyeb控制面板的日志标签

3. **查看完整文档**
   - 详见 `KOYEB_DEPLOYMENT_GUIDE.md`

4. **联系支持**
   - Koyeb支持: https://www.koyeb.com/support
   - GitHub Issues: 提交问题报告

---

**祝部署顺利！🎉**
