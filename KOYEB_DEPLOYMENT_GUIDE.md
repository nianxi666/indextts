# Koyeb GPU H100 部署指南

本指南根据 [Koyeb官方文档](https://www.koyeb.com/docs) 提供了使用curl或JavaScript部署带GPU（H100）的IndexTTS容器的完整说明。

## 前置条件

- Koyeb账户及API密钥
- Docker镜像或GitHub仓库
- curl或Node.js环境

## 快速开始

### 方案1: 使用curl部署

#### 步骤1: 基本部署

```bash
# 设置API密钥和其他配置
export KOYEB_API_KEY="d5yqxgmxn08waujluulb2iczhsfi4kic1lfob7rs1skim4h2jajyxkiospyuxjex"
export DEPLOYMENT_NAME="indextts-gpu-h100"
export INSTANCE_TYPE="gpu-h100"
export CONTAINER_PORT=7860

# 执行部署脚本
bash deploy-koyeb-gpu-h100.sh
```

#### 步骤2: 直接使用curl命令

```bash
API_KEY="d5yqxgmxn08waujluulb2iczhsfi4kic1lfob7rs1skim4h2jajyxkiospyuxjex"

curl -X POST https://app.koyeb.com/v1/deployments \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "displayName": "indextts-gpu-h100",
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
    },
    "instance": {
      "type": "gpu-h100"
    },
    "name": "indextts-gpu-h100"
  }'
```

### 方案2: 使用JavaScript部署

#### 步骤1: 安装依赖（如需）

```bash
# 此脚本使用Node.js内置模块，无需额外依赖
node deploy-koyeb-gpu-h100.js
```

#### 步骤2: 运行部署

```bash
# 执行部署
node deploy-koyeb-gpu-h100.js

# 查看部署状态（需要替换为实际的部署ID）
node deploy-koyeb-gpu-h100.js status <deployment-id>

# 列出所有部署
node deploy-koyeb-gpu-h100.js list
```

## 部署配置详解

### 实例类型（Instance Type）

支持的H100 GPU实例类型：

| 实例类型 | GPU | VRAM | 用途 |
|---------|-----|------|------|
| `gpu-h100` | NVIDIA H100 | 80GB | 高性能AI推理和训练 |
| `gpu-a100` | NVIDIA A100 | 40GB | 中等性能AI任务 |
| `gpu-t4` | NVIDIA T4 | 16GB | 通用GPU计算 |

### 资源配置

```json
{
  "resources": {
    "memory": "16Gi",      // 系统内存
    "cpu": "8"             // CPU核心数
  }
}
```

### 环境变量

| 变量名 | 说明 | 示例 |
|-------|------|------|
| `GRADIO_SERVER_NAME` | Gradio服务器地址 | `0.0.0.0` |
| `GRADIO_SERVER_PORT` | Gradio服务器端口 | `7860` |
| `HF_TOKEN` | Hugging Face令牌（可选） | `hf_...` |

## 部署操作

### 检查部署状态

```bash
# 使用curl
curl https://app.koyeb.com/v1/deployments/<deployment-id> \
  -H "Authorization: Bearer $API_KEY"

# 使用JavaScript脚本
node deploy-koyeb-gpu-h100.js status <deployment-id>
```

### 列出所有部署

```bash
# 使用curl
curl https://app.koyeb.com/v1/deployments \
  -H "Authorization: Bearer $API_KEY"

# 使用JavaScript脚本
node deploy-koyeb-gpu-h100.js list
```

### 删除部署

```bash
curl -X DELETE https://app.koyeb.com/v1/deployments/<deployment-id> \
  -H "Authorization: Bearer $API_KEY"
```

## Docker镜像构建

如果需要使用自定义Docker镜像：

```bash
# 构建镜像
docker build -t your-org/indextts:latest .

# 推送到Docker Hub或其他仓库
docker push your-org/indextts:latest
```

## 故障排除

### 问题1: 部署失败 - 401 Unauthorized

**解决方案：** 检查API密钥是否正确

```bash
# 验证API密钥
curl https://app.koyeb.com/v1/account \
  -H "Authorization: Bearer $API_KEY"
```

### 问题2: 部署失败 - 400 Bad Request

**解决方案：** 验证JSON配置格式，检查所需字段

```bash
# 使用jq验证JSON格式
echo '{"key": "value"}' | jq .
```

### 问题3: GPU不可用

**解决方案：** 
- 确认选择了正确的实例类型（`gpu-h100`）
- 检查账户是否有GPU配额
- 查看部署日志中的错误信息

### 问题4: 应用无法启动

**解决方案：**
- 检查Dockerfile和依赖
- 查看应用日志
- 确认健康检查配置

```bash
# 查看部署日志
curl https://app.koyeb.com/v1/deployments/<deployment-id>/logs \
  -H "Authorization: Bearer $API_KEY"
```

## API文档参考

### 创建部署

```
POST /v1/deployments
```

请求体示例：

```json
{
  "displayName": "string",
  "deployment": {
    "containerPort": integer,
    "docker": {
      "command": ["string"],
      "dockerfile": "string",
      "entrypoint": ["string"]
    },
    "env": [
      {
        "key": "string",
        "value": "string"
      }
    ],
    "resources": {
      "memory": "string",
      "cpu": "string"
    },
    "ports": [
      {
        "port": integer,
        "protocol": "string"
      }
    ]
  },
  "git": {
    "branch": "string",
    "repository": "string"
  },
  "instance": {
    "type": "string"
  },
  "name": "string"
}
```

### 获取部署详情

```
GET /v1/deployments/{deploymentId}
```

响应示例：

```json
{
  "id": "string",
  "displayName": "string",
  "status": "active|inactive|error",
  "url": "string",
  "createdAt": "timestamp",
  "updatedAt": "timestamp"
}
```

## 监控和维护

### 监控应用性能

1. 访问Koyeb控制面板
2. 查看实时日志和指标
3. 配置告警

### 更新部署

```bash
# 更新部署配置
curl -X PATCH https://app.koyeb.com/v1/deployments/<deployment-id> \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "deployment": {
      "resources": {
        "memory": "32Gi",
        "cpu": "16"
      }
    }
  }'
```

## 最佳实践

1. **安全性**
   - 不要在代码中硬编码API密钥
   - 使用环境变量存储敏感信息
   - 定期轮换API密钥

2. **性能优化**
   - 选择合适的实例类型
   - 设置适当的资源限制
   - 使用缓存优化推理速度

3. **监控和日志**
   - 启用详细日志
   - 配置健康检查
   - 定期检查资源使用情况

4. **成本控制**
   - 监控GPU使用时间
   - 及时删除不使用的部署
   - 选择成本效益最高的实例类型

## 更多资源

- [Koyeb官方文档](https://www.koyeb.com/docs)
- [Koyeb API参考](https://www.koyeb.com/docs/api)
- [IndexTTS项目](https://github.com/your-org/indextts)
- [NVIDIA H100 GPU文档](https://www.nvidia.com/en-us/data-center/h100/)

## 支持

如遇到问题，请：

1. 查看[常见问题解答](#故障排除)
2. 访问[Koyeb支持中心](https://www.koyeb.com/support)
3. 查看应用日志获取详细错误信息
4. 联系Koyeb技术支持团队

---

**注意：** 确保将示例中的API密钥、GitHub仓库URL等替换为实际的值。
