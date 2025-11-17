#!/usr/bin/env python3
"""
部署测试脚本 - 验证部署配置和API连接
"""

import os
import sys
import json

# 激活虚拟环境中的requests
try:
    import requests
    print("✓ requests库已导入")
except ImportError:
    print("✗ 需要安装requests库: pip install requests")
    sys.exit(1)

def test_api_connection():
    """测试API连接"""
    print("\n" + "="*60)
    print("测试1: Koyeb API连接")
    print("="*60)
    
    api_key = os.getenv('KOYEB_API_KEY')
    if not api_key:
        print("✗ 未设置 KOYEB_API_KEY 环境变量")
        print("  请设置: export KOYEB_API_KEY='你的密钥'")
        return False
    
    print(f"✓ API密钥已设置: {api_key[:10]}...{api_key[-10:]}")
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get(
            'https://app.koyeb.com/v1/account',
            headers=headers,
            timeout=5
        )
        
        if response.status_code == 200:
            print("✓ API连接成功")
            account = response.json()
            print(f"  账户信息: {json.dumps(account, indent=2, ensure_ascii=False)}")
            return True
        else:
            print(f"✗ API返回错误: {response.status_code}")
            print(f"  响应: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"✗ API连接失败: {e}")
        return False

def test_deployment_config():
    """测试部署配置"""
    print("\n" + "="*60)
    print("测试2: 部署配置验证")
    print("="*60)
    
    config = {
        "displayName": "indextts-gpu-h100-test",
        "name": "indextts-gpu-h100-test",
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
            "repository": "https://github.com/your-org/indextts"
        }
    }
    
    print("✓ 部署配置已创建:")
    print(json.dumps(config, indent=2, ensure_ascii=False))
    
    # 验证JSON
    try:
        json_str = json.dumps(config)
        print(f"\n✓ JSON格式验证通过 (大小: {len(json_str)} bytes)")
        return config
    except Exception as e:
        print(f"✗ JSON格式错误: {e}")
        return None

def show_next_steps():
    """显示下一步操作"""
    print("\n" + "="*60)
    print("下一步操作")
    print("="*60)
    
    print("""
1. 如果以上测试都通过，可以执行实际部署:

   python3 deploy_koyeb_gpu_h100.py deploy \\
     --git-repo https://github.com/your-org/indextts \\
     --wait

2. 或使用curl直接部署:

   bash deploy-koyeb-gpu-h100.sh

3. 或使用Node.js:

   node deploy-koyeb-gpu-h100.js

4. 查看部署状态:

   python3 deploy_koyeb_gpu_h100.py status <deployment-id>
    """)

def main():
    print("""
╔════════════════════════════════════════════════════════╗
║  Koyeb GPU H100 部署 - 测试脚本                         ║
║  Test Script for Koyeb GPU H100 Deployment             ║
╚════════════════════════════════════════════════════════╝
    """)
    
    # 运行测试
    api_ok = test_api_connection()
    config = test_deployment_config()
    
    if not api_ok:
        print("\n❌ API连接失败，无法继续")
        print("请检查:")
        print("  1. API密钥是否正确")
        print("  2. 网络连接是否正常")
        print("  3. Koyeb服务是否可用")
        sys.exit(1)
    
    if not config:
        print("\n❌ 部署配置验证失败")
        sys.exit(1)
    
    print("\n✅ 所有测试通过！")
    show_next_steps()

if __name__ == '__main__':
    main()
