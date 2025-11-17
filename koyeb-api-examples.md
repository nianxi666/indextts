# Koyeb API H100 GPU部署示例

本文档包含使用Koyeb官方API部署带H100 GPU容器的完整示例。

## 目录
1. [基本配置](#基本配置)
2. [curl示例](#curl示例)
3. [JavaScript/Node.js示例](#javascriptnodejs示例)
4. [Python示例](#python示例)
5. [高级配置](#高级配置)
6. [故障排除](#故障排除)

---

## 基本配置

### 必需信息
```
API密钥: d5yqxgmxn08waujluulb2iczhsfi4kic1lfob7rs1skim4h2jajyxkiospyuxjex
API端点: https://app.koyeb.com/v1
GPU类型: H100 (Instance Type: gpu-h100)
应用端口: 7860 (Gradio默认端口)
```

### API认证
所有请求都需要在Header中包含认证信息：
```
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
```

---

## curl示例

### 1. 创建部署 (从Git仓库)

```bash
#!/bin/bash

API_KEY="d5yqxgmxn08waujluulb2iczhsfi4kic1lfob7rs1skim4h2jajyxkiospyuxjex"
DEPLOYMENT_NAME="indextts-gpu-h100"
GIT_REPO="https://github.com/your-org/indextts"
GIT_BRANCH="main"

curl -X POST https://app.koyeb.com/v1/deployments \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "displayName": "'$DEPLOYMENT_NAME'",
    "name": "'$DEPLOYMENT_NAME'",
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
        },
        {
          "key": "PYTHONUNBUFFERED",
          "value": "1"
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
      "branch": "'$GIT_BRANCH'",
      "repository": "'$GIT_REPO'"
    }
  }' | jq .
```

### 2. 创建部署 (从Docker镜像)

```bash
API_KEY="d5yqxgmxn08waujluulb2iczhsfi4kic1lfob7rs1skim4h2jajyxkiospyuxjex"

curl -X POST https://app.koyeb.com/v1/deployments \
  -H "Authorization: Bearer $API_KEY" \
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
        "image": "your-org/indextts:latest",
        "entrypoint": []
      },
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
    }
  }' | jq .
```

### 3. 获取部署列表

```bash
API_KEY="d5yqxgmxn08waujluulb2iczhsfi4kic1lfob7rs1skim4h2jajyxkiospyuxjex"

curl -X GET https://app.koyeb.com/v1/deployments \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" | jq .
```

### 4. 获取单个部署详情

```bash
API_KEY="d5yqxgmxn08waujluulb2iczhsfi4kic1lfob7rs1skim4h2jajyxkiospyuxjex"
DEPLOYMENT_ID="abc123xyz"

curl -X GET https://app.koyeb.com/v1/deployments/$DEPLOYMENT_ID \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" | jq .
```

### 5. 删除部署

```bash
API_KEY="d5yqxgmxn08waujluulb2iczhsfi4kic1lfob7rs1skim4h2jajyxkiospyuxjex"
DEPLOYMENT_ID="abc123xyz"

curl -X DELETE https://app.koyeb.com/v1/deployments/$DEPLOYMENT_ID \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json"
```

### 6. 更新部署

```bash
API_KEY="d5yqxgmxn08waujluulb2iczhsfi4kic1lfob7rs1skim4h2jajyxkiospyuxjex"
DEPLOYMENT_ID="abc123xyz"

curl -X PATCH https://app.koyeb.com/v1/deployments/$DEPLOYMENT_ID \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "deployment": {
      "resources": {
        "memory": "32Gi",
        "cpu": "16"
      }
    }
  }' | jq .
```

---

## JavaScript/Node.js示例

### 1. 基本部署脚本

```javascript
const https = require('https');

function deployToKoyeb() {
  const apiKey = 'd5yqxgmxn08waujluulb2iczhsfi4kic1lfob7rs1skim4h2jajyxkiospyuxjex';
  
  const deploymentConfig = {
    displayName: 'indextts-gpu-h100',
    name: 'indextts-gpu-h100',
    instance: {
      type: 'gpu-h100'
    },
    deployment: {
      containerPort: 7860,
      docker: {
        command: ['python', 'webui.py', '--host', '0.0.0.0', '--port', '7860'],
        dockerfile: 'Dockerfile'
      },
      env: [
        { key: 'GRADIO_SERVER_NAME', value: '0.0.0.0' },
        { key: 'GRADIO_SERVER_PORT', value: '7860' }
      ],
      resources: {
        memory: '16Gi',
        cpu: '8'
      },
      ports: [{ port: 7860, protocol: 'http' }]
    },
    git: {
      branch: 'main',
      repository: 'https://github.com/your-org/indextts'
    }
  };

  const data = JSON.stringify(deploymentConfig);
  
  const options = {
    hostname: 'app.koyeb.com',
    port: 443,
    path: '/v1/deployments',
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
      'Content-Length': data.length
    }
  };

  const req = https.request(options, (res) => {
    let responseData = '';

    res.on('data', (chunk) => {
      responseData += chunk;
    });

    res.on('end', () => {
      console.log('Response Status:', res.statusCode);
      console.log('Response Data:', JSON.parse(responseData));
    });
  });

  req.on('error', (e) => {
    console.error(`Problem with request: ${e.message}`);
  });

  req.write(data);
  req.end();
}

deployToKoyeb();
```

### 2. 获取部署状态

```javascript
const https = require('https');

function getDeploymentStatus(deploymentId) {
  const apiKey = 'd5yqxgmxn08waujluulb2iczhsfi4kic1lfob7rs1skim4h2jajyxkiospyuxjex';

  const options = {
    hostname: 'app.koyeb.com',
    port: 443,
    path: `/v1/deployments/${deploymentId}`,
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json'
    }
  };

  const req = https.request(options, (res) => {
    let responseData = '';

    res.on('data', (chunk) => {
      responseData += chunk;
    });

    res.on('end', () => {
      const deployment = JSON.parse(responseData);
      console.log('Deployment Status:', deployment.status);
      console.log('URL:', deployment.url);
      console.log('Created At:', deployment.createdAt);
    });
  });

  req.on('error', (e) => {
    console.error(`Problem with request: ${e.message}`);
  });

  req.end();
}

// 使用示例
getDeploymentStatus('abc123xyz');
```

### 3. 完整的部署管理器类

```javascript
class KoyebDeploymentManager {
  constructor(apiKey) {
    this.apiKey = apiKey;
    this.baseUrl = 'https://app.koyeb.com/v1';
  }

  async makeRequest(method, path, data = null) {
    return new Promise((resolve, reject) => {
      const url = new URL(this.baseUrl + path);
      
      const options = {
        hostname: url.hostname,
        port: url.port,
        path: url.pathname,
        method: method,
        headers: {
          'Authorization': `Bearer ${this.apiKey}`,
          'Content-Type': 'application/json'
        }
      };

      if (data) {
        options.headers['Content-Length'] = Buffer.byteLength(data);
      }

      const req = https.request(options, (res) => {
        let responseData = '';

        res.on('data', (chunk) => {
          responseData += chunk;
        });

        res.on('end', () => {
          resolve({
            status: res.statusCode,
            data: JSON.parse(responseData)
          });
        });
      });

      req.on('error', reject);

      if (data) {
        req.write(data);
      }

      req.end();
    });
  }

  async createDeployment(config) {
    const response = await this.makeRequest('POST', '/deployments', JSON.stringify(config));
    return response.data;
  }

  async listDeployments() {
    const response = await this.makeRequest('GET', '/deployments');
    return response.data;
  }

  async getDeployment(deploymentId) {
    const response = await this.makeRequest('GET', `/deployments/${deploymentId}`);
    return response.data;
  }

  async deleteDeployment(deploymentId) {
    const response = await this.makeRequest('DELETE', `/deployments/${deploymentId}`);
    return response.status === 204;
  }
}

// 使用示例
const manager = new KoyebDeploymentManager('d5yqxgmxn08waujluulb2iczhsfi4kic1lfob7rs1skim4h2jajyxkiospyuxjex');

const config = {
  displayName: 'indextts-gpu-h100',
  name: 'indextts-gpu-h100',
  instance: { type: 'gpu-h100' },
  deployment: {
    containerPort: 7860,
    docker: {
      command: ['python', 'webui.py', '--host', '0.0.0.0', '--port', '7860'],
      dockerfile: 'Dockerfile'
    },
    resources: { memory: '16Gi', cpu: '8' },
    ports: [{ port: 7860, protocol: 'http' }]
  },
  git: {
    branch: 'main',
    repository: 'https://github.com/your-org/indextts'
  }
};

manager.createDeployment(config)
  .then(result => console.log('Deployment created:', result.id))
  .catch(err => console.error('Error:', err));
```

---

## Python示例

### 1. 使用requests库

```python
import requests
import json

def deploy_to_koyeb():
    api_key = 'd5yqxgmxn08waujluulb2iczhsfi4kic1lfob7rs1skim4h2jajyxkiospyuxjex'
    api_url = 'https://app.koyeb.com/v1/deployments'
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    deployment_config = {
        'displayName': 'indextts-gpu-h100',
        'name': 'indextts-gpu-h100',
        'instance': {
            'type': 'gpu-h100'
        },
        'deployment': {
            'containerPort': 7860,
            'docker': {
                'command': ['python', 'webui.py', '--host', '0.0.0.0', '--port', '7860'],
                'dockerfile': 'Dockerfile'
            },
            'env': [
                {'key': 'GRADIO_SERVER_NAME', 'value': '0.0.0.0'},
                {'key': 'GRADIO_SERVER_PORT', 'value': '7860'}
            ],
            'resources': {
                'memory': '16Gi',
                'cpu': '8'
            },
            'ports': [{'port': 7860, 'protocol': 'http'}]
        },
        'git': {
            'branch': 'main',
            'repository': 'https://github.com/your-org/indextts'
        }
    }
    
    response = requests.post(api_url, headers=headers, json=deployment_config)
    
    if response.status_code >= 200 and response.status_code < 300:
        print('Deployment successful!')
        print(json.dumps(response.json(), indent=2))
    else:
        print(f'Deployment failed: {response.status_code}')
        print(response.text)

if __name__ == '__main__':
    deploy_to_koyeb()
```

### 2. 获取部署列表

```python
import requests

def list_deployments():
    api_key = 'd5yqxgmxn08waujluulb2iczhsfi4kic1lfob7rs1skim4h2jajyxkiospyuxjex'
    api_url = 'https://app.koyeb.com/v1/deployments'
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    response = requests.get(api_url, headers=headers)
    deployments = response.json()
    
    for deployment in deployments.get('deployments', []):
        print(f"ID: {deployment['id']}")
        print(f"Name: {deployment['displayName']}")
        print(f"Status: {deployment['status']}")
        print(f"URL: {deployment.get('url', 'N/A')}")
        print('---')

if __name__ == '__main__':
    list_deployments()
```

---

## 高级配置

### 1. 环境变量配置

```json
{
  "env": [
    {"key": "GRADIO_SERVER_NAME", "value": "0.0.0.0"},
    {"key": "GRADIO_SERVER_PORT", "value": "7860"},
    {"key": "PYTHONUNBUFFERED", "value": "1"},
    {"key": "HF_TOKEN", "value": "hf_xxxxx"},
    {"key": "CUDA_VISIBLE_DEVICES", "value": "0"},
    {"key": "TORCH_HOME", "value": "/app/torch_cache"},
    {"key": "HF_HOME", "value": "/app/hf_cache"}
  ]
}
```

### 2. 不同的实例类型

```json
{
  "instance": {
    "type": "gpu-h100"    // NVIDIA H100 - 高性能
  }
}
```

其他可用的GPU实例：
- `gpu-a100`: NVIDIA A100
- `gpu-t4`: NVIDIA T4
- `cpu`: CPU实例

### 3. 自定义启动命令

```json
{
  "deployment": {
    "docker": {
      "command": [
        "python",
        "webui.py",
        "--host",
        "0.0.0.0",
        "--port",
        "7860",
        "--fp16",
        "--deepspeed"
      ],
      "dockerfile": "Dockerfile",
      "entrypoint": []
    }
  }
}
```

---

## 故障排除

### 问题：401 Unauthorized

**原因**: API密钥无效或已过期

**解决方案**:
```bash
# 验证API密钥
curl https://app.koyeb.com/v1/account \
  -H "Authorization: Bearer $API_KEY"
```

### 问题：400 Bad Request

**原因**: JSON格式错误或缺少必需字段

**解决方案**:
```bash
# 验证JSON格式
echo '{"key": "value"}' | jq .

# 检查必需字段
# - displayName
# - name
# - instance.type
# - deployment.containerPort
```

### 问题：GPU不可用

**原因**: 账户无GPU配额或实例类型不可用

**解决方案**:
1. 检查Koyeb账户设置
2. 验证GPU配额
3. 尝试使用不同的实例类型

### 问题：部署失败

**原因**: Dockerfile或依赖问题

**解决方案**:
1. 检查Dockerfile是否有效
2. 验证所有依赖都已列出
3. 查看部署日志获取详细信息

---

## 安全最佳实践

1. **API密钥管理**
   - 使用环境变量存储API密钥
   - 定期轮换API密钥
   - 不要提交密钥到版本控制系统

2. **仓库安全**
   - 使用私有GitHub仓库
   - 实现访问控制
   - 审计日志

3. **应用安全**
   - 使用HTTPS
   - 实施认证和授权
   - 定期更新依赖

---

更多信息，请参考官方文档: https://www.koyeb.com/docs
