#!/usr/bin/env python3
"""
Koyeb自动部署脚本 - IndexTTS WebUI
使用Koyeb REST API进行自动部署
"""

import os
import sys
import json
import time
import requests
from urllib.parse import urljoin

# 配置
GITHUB_REPO = "https://github.com/nianxi666/indextts"
BRANCH = "koyeb-deploy-gpu-a4000-github-define-python"
SERVICE_NAME = "indextts-webui"
KOYEB_API_TOKEN = os.environ.get("KOYEB_API_TOKEN", "rocrorea70dhiis0zw0u68j35xve4ljjpt6ytw2sz7ixbr8y70ox7dpgqj497h28")
KOYEB_API_URL = "https://app.koyeb.com/v1"

# 颜色定义
class Colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text):
    """打印标题"""
    print(f"\n{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}{text}{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.END}\n")

def print_success(text):
    """打印成功信息"""
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")

def print_error(text):
    """打印错误信息"""
    print(f"{Colors.RED}❌ {text}{Colors.END}")

def print_warning(text):
    """打印警告信息"""
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.END}")

def print_info(text):
    """打印信息"""
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.END}")

def verify_token():
    """验证API令牌"""
    print_info("验证Koyeb API令牌...")
    
    if not KOYEB_API_TOKEN:
        print_error("KOYEB_API_TOKEN未设置")
        print_info("请运行: export KOYEB_API_TOKEN='你的令牌'")
        sys.exit(1)
    
    headers = {
        "Authorization": f"Bearer {KOYEB_API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(f"{KOYEB_API_URL}/account", headers=headers, timeout=10)
        
        if response.status_code == 200:
            print_success("API令牌有效")
            return True
        else:
            print_error("API令牌无效或过期")
            print_info(f"状态码: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"验证失败: {str(e)}")
        return False

def check_existing_service():
    """检查服务是否已存在"""
    print_info("检查服务是否已存在...")
    
    headers = {
        "Authorization": f"Bearer {KOYEB_API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(f"{KOYEB_API_URL}/services", headers=headers, timeout=10)
        
        if response.status_code == 200:
            services = response.json().get("services", [])
            for service in services:
                if service.get("name") == SERVICE_NAME:
                    print_warning(f"服务 '{SERVICE_NAME}' 已存在")
                    return True
            
            print_success("这是新部署")
            return False
    except Exception as e:
        print_warning(f"检查失败: {str(e)}")
        return False

def deploy_service():
    """创建部署"""
    print_header("🚀 开始部署")
    
    print(f"服务名称: {SERVICE_NAME}")
    print(f"GitHub仓库: {GITHUB_REPO}")
    print(f"分支: {BRANCH}")
    print()
    
    headers = {
        "Authorization": f"Bearer {KOYEB_API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    deployment_data = {
        "name": SERVICE_NAME,
        "git": {
            "repository": GITHUB_REPO,
            "branch": BRANCH
        },
        "instance_type": "gpu-a4000",
        "regions": ["fra"],
        "ports": [
            {
                "port": 7860,
                "protocol": "http",
                "public": True
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
        ]
    }
    
    try:
        print_info("发送部署请求...")
        response = requests.post(
            f"{KOYEB_API_URL}/services",
            headers=headers,
            json=deployment_data,
            timeout=30
        )
        
        if response.status_code in [200, 201]:
            service_data = response.json()
            service_id = service_data.get("id") or service_data.get("service", {}).get("id")
            
            print_success("部署请求已发送")
            if service_id:
                print_info(f"服务ID: {service_id}")
            
            return True
        else:
            print_error(f"部署失败 (状态码: {response.status_code})")
            print_info(f"响应: {response.text}")
            return False
    
    except Exception as e:
        print_error(f"部署请求失败: {str(e)}")
        return False

def show_deployment_info():
    """显示部署信息"""
    print_header("✅ 部署已启动")
    
    print(f"{Colors.BOLD}📋 部署信息:{Colors.END}")
    print(f"  服务名称: {SERVICE_NAME}")
    print(f"  分支: {BRANCH}")
    print(f"  GPU: NVIDIA A4000")
    print(f"  Python: 3.10")
    print(f"  端口: 7860")
    print()
    
    print(f"{Colors.BOLD}⏱️ 预期时间:{Colors.END}")
    print(f"  首次启动: 20-45分钟")
    print(f"  后续启动: 2-5分钟")
    print()
    
    print(f"{Colors.BOLD}📊 监控部署:{Colors.END}")
    print(f"  访问: {Colors.BLUE}https://app.koyeb.com{Colors.END}")
    print(f"  查看日志: 在服务详情页面")
    print()
    
    print(f"{Colors.BOLD}🎯 部署完成后:{Colors.END}")
    print(f"  1. Koyeb会分配一个公开URL")
    print(f"  2. 在浏览器中打开该URL")
    print(f"  3. 开始使用IndexTTS WebUI")
    print()

def main():
    """主函数"""
    print_header("🚀 IndexTTS WebUI Koyeb自动部署脚本")
    
    # 验证令牌
    if not verify_token():
        sys.exit(1)
    
    print()
    
    # 检查现有服务
    check_existing_service()
    
    print()
    
    # 部署
    if not deploy_service():
        sys.exit(1)
    
    print()
    
    # 显示信息
    show_deployment_info()
    
    print(f"{Colors.GREEN}✅ 部署过程已完成！{Colors.END}")
    print()
    print(f"{Colors.BOLD}后续步骤:{Colors.END}")
    print(f"1. 打开 {Colors.BLUE}https://app.koyeb.com{Colors.END}")
    print(f"2. 查看服务进度")
    print(f"3. 等待部署完成")
    print(f"4. 获取应用URL并开始使用")
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_warning("用户中断")
        sys.exit(1)
    except Exception as e:
        print_error(f"发生错误: {str(e)}")
        sys.exit(1)
