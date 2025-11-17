#!/bin/bash

# Koyeb GPU H100 部署脚本
# 根据Koyeb官方文档: https://www.koyeb.com/docs
# 使用curl部署带GPU（H100）的容器

set -e

# 配置信息
API_KEY="d5yqxgmxn08waujluulb2iczhsfi4kic1lfob7rs1skim4h2jajyxkiospyuxjex"
KOYEB_API_URL="https://app.koyeb.com/v1"

# 容器配置
CONTAINER_IMAGE="python:3.11"  # 基础镜像，可根据需要修改
DEPLOYMENT_NAME="indextts-gpu-h100"
INSTANCE_TYPE="gpu-h100"  # H100 GPU实例类型
PORT=7860
MEMORY="16Gi"
CPU="8"

# 部署函数
deploy_with_curl() {
    echo "开始使用curl部署IndexTTS到Koyeb（GPU H100）..."
    
    # 步骤1: 创建部署配置JSON
    DEPLOYMENT_CONFIG=$(cat <<EOF
{
  "displayName": "${DEPLOYMENT_NAME}",
  "deployment": {
    "containerPort": ${PORT},
    "docker": {
      "command": [
        "python",
        "webui.py",
        "--host",
        "0.0.0.0",
        "--port",
        "${PORT}"
      ],
      "dockerfile": "Dockerfile",
      "entrypoint": []
    },
    "env": [
      {
        "key": "HF_TOKEN",
        "value": "${HF_TOKEN:-}"
      }
    ],
    "resources": {
      "memory": "${MEMORY}",
      "cpu": "${CPU}"
    },
    "ports": [
      {
        "port": ${PORT},
        "protocol": "http"
      }
    ]
  },
  "git": {
    "branch": "main",
    "repository": "https://github.com/your-org/indextts"
  },
  "instance": {
    "type": "${INSTANCE_TYPE}"
  },
  "name": "${DEPLOYMENT_NAME}"
}
EOF
)

    # 步骤2: 创建应用和部署
    echo "创建Koyeb应用部署..."
    
    RESPONSE=$(curl -X POST \
      "${KOYEB_API_URL}/deployments" \
      -H "Authorization: Bearer ${API_KEY}" \
      -H "Content-Type: application/json" \
      -d "${DEPLOYMENT_CONFIG}")
    
    echo "响应: ${RESPONSE}"
    
    # 提取部署ID
    DEPLOYMENT_ID=$(echo "${RESPONSE}" | grep -o '"id":"[^"]*"' | head -1 | cut -d'"' -f4)
    
    if [ -z "${DEPLOYMENT_ID}" ]; then
        echo "错误: 无法获取部署ID"
        return 1
    fi
    
    echo "部署成功！部署ID: ${DEPLOYMENT_ID}"
    echo "请访问Koyeb控制面板查看部署状态: ${KOYEB_API_URL}/deployments/${DEPLOYMENT_ID}"
}

# 检查部署状态
check_deployment_status() {
    local DEPLOYMENT_ID=$1
    
    echo "检查部署状态..."
    
    curl -X GET \
      "${KOYEB_API_URL}/deployments/${DEPLOYMENT_ID}" \
      -H "Authorization: Bearer ${API_KEY}" \
      -H "Content-Type: application/json"
}

# 主程序
if [ $# -eq 0 ]; then
    deploy_with_curl
else
    case "$1" in
        status)
            if [ -z "$2" ]; then
                echo "用法: $0 status <deployment-id>"
                exit 1
            fi
            check_deployment_status "$2"
            ;;
        *)
            echo "未知命令: $1"
            echo "用法: $0 [status <deployment-id>]"
            exit 1
            ;;
    esac
fi
