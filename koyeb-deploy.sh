#!/bin/bash

# ========================================
# Koyeb GPU H100 一键部署脚本
# Koyeb GPU H100 One-Click Deployment Script
# ========================================

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

log_error() {
    echo -e "${RED}[✗]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

# 显示标题
show_banner() {
    clear
    echo "╔════════════════════════════════════════════════════════╗"
    echo "║  Koyeb GPU H100 一键部署工具                           ║"
    echo "║  Koyeb GPU H100 One-Click Deployment Tool              ║"
    echo "╚════════════════════════════════════════════════════════╝"
    echo ""
}

# 检查依赖
check_dependencies() {
    log_info "检查依赖环境..."
    
    if ! command -v curl &> /dev/null; then
        log_error "curl未安装，请先安装: apt install curl"
        exit 1
    fi
    log_success "curl已安装"
    
    if ! command -v python3 &> /dev/null; then
        log_error "python3未安装"
        exit 1
    fi
    log_success "python3已安装"
    
    if ! command -v jq &> /dev/null; then
        log_warning "jq未安装，部分功能可能受限"
        HAS_JQ=false
    else
        log_success "jq已安装"
        HAS_JQ=true
    fi
}

# 检查Python依赖
check_python_deps() {
    python3 -c "import requests" 2>/dev/null && return 0
    
    log_warning "需要安装Python requests库"
    log_info "正在安装requests..."
    
    if pip3 install --user requests 2>/dev/null; then
        log_success "requests已安装"
        return 0
    elif pip3 install --break-system-packages requests 2>/dev/null; then
        log_success "requests已安装"
        return 0
    else
        log_error "无法安装requests库"
        return 1
    fi
}

# 配置部署参数
configure_deployment() {
    log_info "配置部署参数..."
    
    # API密钥
    if [ -z "$KOYEB_API_KEY" ]; then
        read -p "请输入Koyeb API密钥: " KOYEB_API_KEY
    fi
    
    if [ -z "$KOYEB_API_KEY" ]; then
        log_error "API密钥不能为空"
        exit 1
    fi
    log_success "API密钥已设置"
    
    # Git仓库
    if [ -z "$GIT_REPO" ]; then
        read -p "请输入Git仓库URL (例如: https://github.com/user/indextts): " GIT_REPO
    fi
    
    if [ -z "$GIT_REPO" ]; then
        log_error "Git仓库URL不能为空"
        exit 1
    fi
    log_success "Git仓库: $GIT_REPO"
    
    # 部署名称
    DEPLOYMENT_NAME="${DEPLOYMENT_NAME:-indextts-gpu-h100}"
    log_success "部署名称: $DEPLOYMENT_NAME"
    
    # GPU实例
    INSTANCE_TYPE="${INSTANCE_TYPE:-gpu-h100}"
    log_success "GPU类型: $INSTANCE_TYPE"
    
    # 资源配置
    MEMORY="${MEMORY:-16Gi}"
    CPU="${CPU:-8}"
    log_success "内存: $MEMORY, CPU: $CPU核心"
}

# 验证API连接
verify_api() {
    log_info "验证Koyeb API连接..."
    
    RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" \
        -H "Authorization: Bearer $KOYEB_API_KEY" \
        "https://app.koyeb.com/v1/deployments")
    
    if [ "$RESPONSE" = "200" ] || [ "$RESPONSE" = "401" ]; then
        log_success "API连接正常"
        return 0
    else
        log_error "API返回错误: HTTP $RESPONSE"
        return 1
    fi
}

# 使用Python脚本部署
deploy_with_python() {
    log_info "准备部署..."
    
    # 检查Python脚本
    if [ ! -f "deploy_koyeb_gpu_h100.py" ]; then
        log_error "deploy_koyeb_gpu_h100.py不存在"
        exit 1
    fi
    
    log_info "执行部署 (这可能需要几分钟)..."
    
    export KOYEB_API_KEY
    
    python3 deploy_koyeb_gpu_h100.py deploy \
        --git-repo "$GIT_REPO" \
        --name "$DEPLOYMENT_NAME" \
        --instance-type "$INSTANCE_TYPE" \
        --memory "$MEMORY" \
        --cpu "$CPU" \
        --wait
}

# 使用curl部署
deploy_with_curl() {
    log_info "准备部署 (curl方式)..."
    
    DEPLOYMENT_CONFIG=$(cat <<EOF
{
  "displayName": "$DEPLOYMENT_NAME",
  "name": "$DEPLOYMENT_NAME",
  "instance": {
    "type": "$INSTANCE_TYPE"
  },
  "deployment": {
    "containerPort": 7860,
    "docker": {
      "command": ["python", "webui.py", "--host", "0.0.0.0", "--port", "7860"],
      "dockerfile": "Dockerfile"
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
      "memory": "$MEMORY",
      "cpu": "$CPU"
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
    "repository": "$GIT_REPO"
  }
}
EOF
)
    
    log_info "发送部署请求..."
    
    RESPONSE=$(curl -s -X POST https://app.koyeb.com/v1/deployments \
        -H "Authorization: Bearer $KOYEB_API_KEY" \
        -H "Content-Type: application/json" \
        -d "$DEPLOYMENT_CONFIG")
    
    echo "$RESPONSE"
    
    if [ "$HAS_JQ" = true ]; then
        DEPLOYMENT_ID=$(echo "$RESPONSE" | jq -r '.id' 2>/dev/null)
        if [ ! -z "$DEPLOYMENT_ID" ] && [ "$DEPLOYMENT_ID" != "null" ]; then
            log_success "部署已创建！"
            log_info "部署ID: $DEPLOYMENT_ID"
            log_info "查看状态: https://app.koyeb.com/v1/deployments/$DEPLOYMENT_ID"
            
            # 保存部署ID
            echo "$DEPLOYMENT_ID" > .deployment_id
            log_success "部署ID已保存到 .deployment_id"
            
            return 0
        fi
    fi
    
    log_warning "部署命令已发送，请手动查看部署状态"
}

# 显示部署后信息
show_post_deployment() {
    echo ""
    echo "╔════════════════════════════════════════════════════════╗"
    echo "║  部署完成！Next Steps                                   ║"
    echo "╚════════════════════════════════════════════════════════╝"
    echo ""
    log_success "部署已成功！"
    echo ""
    log_info "后续操作:"
    echo ""
    echo "  1. 查看部署状态:"
    echo "     python3 deploy_koyeb_gpu_h100.py status <deployment-id>"
    echo ""
    echo "  2. 列出所有部署:"
    echo "     python3 deploy_koyeb_gpu_h100.py list"
    echo ""
    echo "  3. 删除部署:"
    echo "     python3 deploy_koyeb_gpu_h100.py delete <deployment-id>"
    echo ""
    echo "  4. 查看完整文档:"
    echo "     cat QUICK_START_DEPLOY.md"
    echo "     cat KOYEB_DEPLOYMENT_GUIDE.md"
    echo ""
    log_warning "H100 GPU部署会产生成本，不使用时请及时删除！"
    echo ""
}

# 主函数
main() {
    show_banner
    
    # 获取脚本目录
    SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
    cd "$SCRIPT_DIR"
    
    # 检查依赖
    check_dependencies
    echo ""
    
    # 配置参数
    configure_deployment
    echo ""
    
    # 验证API
    if ! verify_api; then
        log_warning "API验证失败，但仍然尝试部署"
    fi
    echo ""
    
    # 选择部署方式
    log_info "选择部署方式..."
    echo "  1) 使用Python脚本 (推荐 - 功能完整)"
    echo "  2) 使用curl (简单快速)"
    
    read -p "请选择 (1-2, 默认: 1): " DEPLOY_METHOD
    DEPLOY_METHOD=${DEPLOY_METHOD:-1}
    echo ""
    
    case $DEPLOY_METHOD in
        1)
            check_python_deps || exit 1
            deploy_with_python
            ;;
        2)
            deploy_with_curl
            ;;
        *)
            log_error "无效的选择"
            exit 1
            ;;
    esac
    
    echo ""
    show_post_deployment
}

# 运行主函数
main "$@"
