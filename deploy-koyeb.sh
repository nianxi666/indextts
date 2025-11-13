#!/bin/bash

################################################################################
# Koyeb自动部署脚本 - IndexTTS WebUI
# 此脚本使用Koyeb API自动部署应用
################################################################################

# 配置
GITHUB_REPO="https://github.com/nianxi666/indextts"
BRANCH="koyeb-deploy-gpu-a4000-github-define-python"
SERVICE_NAME="indextts-webui"
KOYEB_API_TOKEN="${KOYEB_API_TOKEN:-rocrorea70dhiis0zw0u68j35xve4ljjpt6ytw2sz7ixbr8y70ox7dpgqj497h28}"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║    IndexTTS WebUI Koyeb自动部署脚本${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# 检查必要的工具
check_tools() {
    echo -e "${YELLOW}检查必要工具...${NC}"
    
    if ! command -v curl &> /dev/null; then
        echo -e "${RED}❌ 错误: 需要安装curl${NC}"
        exit 1
    fi
    
    if ! command -v git &> /dev/null; then
        echo -e "${RED}❌ 错误: 需要安装git${NC}"
        exit 1
    fi
    
    if ! command -v jq &> /dev/null; then
        echo -e "${YELLOW}⚠️  建议安装jq以解析JSON (可选)${NC}"
    fi
    
    echo -e "${GREEN}✅ 工具检查完成${NC}"
    echo ""
}

# 验证API令牌
verify_token() {
    echo -e "${YELLOW}验证Koyeb API令牌...${NC}"
    
    if [ -z "$KOYEB_API_TOKEN" ]; then
        echo -e "${RED}❌ 错误: KOYEB_API_TOKEN未设置${NC}"
        echo "请运行: export KOYEB_API_TOKEN='你的令牌'"
        exit 1
    fi
    
    # 测试令牌有效性
    RESPONSE=$(curl -s -X GET "https://app.koyeb.com/v1/account" \
        -H "Authorization: Bearer $KOYEB_API_TOKEN" \
        -H "Content-Type: application/json")
    
    if echo "$RESPONSE" | grep -q '"id"'; then
        echo -e "${GREEN}✅ API令牌有效${NC}"
    else
        echo -e "${RED}❌ API令牌无效或过期${NC}"
        exit 1
    fi
    echo ""
}

# 检查服务是否已存在
check_existing_service() {
    echo -e "${YELLOW}检查服务是否已存在...${NC}"
    
    RESPONSE=$(curl -s -X GET "https://app.koyeb.com/v1/services" \
        -H "Authorization: Bearer $KOYEB_API_TOKEN" \
        -H "Content-Type: application/json")
    
    if echo "$RESPONSE" | grep -q "$SERVICE_NAME"; then
        echo -e "${YELLOW}⚠️  服务 '$SERVICE_NAME' 已存在${NC}"
        echo "将进行更新而不是创建新服务"
        SERVICE_EXISTS=true
    else
        echo -e "${GREEN}✅ 这是新部署${NC}"
        SERVICE_EXISTS=false
    fi
    echo ""
}

# 创建部署
deploy_service() {
    echo -e "${YELLOW}开始部署...${NC}"
    echo "服务名称: $SERVICE_NAME"
    echo "GitHub仓库: $GITHUB_REPO"
    echo "分支: $BRANCH"
    echo ""
    
    # 创建部署JSON
    DEPLOYMENT_JSON=$(cat <<EOF
{
  "name": "$SERVICE_NAME",
  "git": {
    "repository": "$GITHUB_REPO",
    "branch": "$BRANCH"
  },
  "instance_type": "gpu-a4000",
  "regions": ["fra"],
  "ports": [
    {
      "port": 7860,
      "protocol": "http",
      "public": true
    }
  ],
  "env": [
    {
      "key": "GRADIO_SHARE",
      "value": "false"
    },
    {
      "key": "HF_HOME",
      "value": "/workspace/.huggingface"
    },
    {
      "key": "TRANSFORMERS_CACHE",
      "value": "/workspace/.cache/transformers"
    }
  ],
  "routes": [
    {
      "path": "/",
      "port_name": "http"
    }
  ]
}
EOF
)

    # 发送部署请求
    RESPONSE=$(curl -s -X POST "https://app.koyeb.com/v1/services" \
        -H "Authorization: Bearer $KOYEB_API_TOKEN" \
        -H "Content-Type: application/json" \
        -d "$DEPLOYMENT_JSON")
    
    # 检查响应
    if echo "$RESPONSE" | grep -q '"id"'; then
        echo -e "${GREEN}✅ 部署请求已发送${NC}"
        
        # 提取服务ID
        SERVICE_ID=$(echo "$RESPONSE" | grep -o '"id":"[^"]*' | head -1 | cut -d'"' -f4)
        
        if [ ! -z "$SERVICE_ID" ]; then
            echo -e "${GREEN}服务ID: $SERVICE_ID${NC}"
        fi
    else
        echo -e "${RED}❌ 部署失败${NC}"
        echo "响应: $RESPONSE"
        exit 1
    fi
    echo ""
}

# 监控部署进度
monitor_deployment() {
    echo -e "${YELLOW}监控部署进度...${NC}"
    echo "提示: 部署通常需要20-45分钟"
    echo "您也可以在 https://app.koyeb.com 的控制面板中查看进度"
    echo ""
    
    # 等待一段时间后查询状态
    sleep 30
    
    RESPONSE=$(curl -s -X GET "https://app.koyeb.com/v1/services" \
        -H "Authorization: Bearer $KOYEB_API_TOKEN" \
        -H "Content-Type: application/json")
    
    # 查找服务状态
    if echo "$RESPONSE" | grep -q "$SERVICE_NAME"; then
        echo -e "${GREEN}✅ 服务已创建，正在部署中...${NC}"
        echo ""
        echo "前往以下链接查看部署进度:"
        echo -e "${BLUE}https://app.koyeb.com/services${NC}"
    fi
}

# 显示部署信息
show_info() {
    echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║              部署已启动！${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${BLUE}📋 部署信息:${NC}"
    echo "  服务名称: $SERVICE_NAME"
    echo "  分支: $BRANCH"
    echo "  GPU: NVIDIA A4000"
    echo "  Python: 3.10"
    echo "  端口: 7860"
    echo ""
    echo -e "${BLUE}⏱️ 预期时间:${NC}"
    echo "  首次启动: 20-45分钟"
    echo "  后续启动: 2-5分钟"
    echo ""
    echo -e "${BLUE}📊 监控部署:${NC}"
    echo "  访问: https://app.koyeb.com"
    echo "  查看日志: 在服务详情页面"
    echo ""
    echo -e "${BLUE}🎯 部署完成后:${NC}"
    echo "  1. Koyeb会分配一个公开URL"
    echo "  2. 在浏览器中打开该URL"
    echo "  3. 开始使用IndexTTS WebUI"
    echo ""
}

# 主函数
main() {
    check_tools
    verify_token
    check_existing_service
    deploy_service
    monitor_deployment
    show_info
    
    echo -e "${GREEN}✅ 部署过程已完成！${NC}"
    echo ""
    echo -e "${YELLOW}后续步骤:${NC}"
    echo "1. 打开 https://app.koyeb.com"
    echo "2. 查看服务进度"
    echo "3. 等待部署完成"
    echo "4. 获取应用URL并开始使用"
}

# 运行主函数
main
