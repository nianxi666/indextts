#!/usr/bin/env python3
"""
验证Koyeb部署配置的脚本
检查所有必要的配置文件和设置
"""

import os
import sys

def check_file_exists(filepath, description):
    """检查文件是否存在"""
    if os.path.exists(filepath):
        size = os.path.getsize(filepath)
        print(f"✅ {description}: {filepath} ({size} bytes)")
        return True
    else:
        print(f"❌ {description}: {filepath} 不存在")
        return False

def check_file_content(filepath, keyword, description):
    """检查文件内容是否包含关键词"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            if keyword in content:
                print(f"✅ {description}")
                return True
            else:
                print(f"❌ {description}：未找到 '{keyword}'")
                return False
    except Exception as e:
        print(f"❌ {description}：读取文件失败 - {e}")
        return False

def main():
    print("=" * 60)
    print("Koyeb 部署配置验证")
    print("=" * 60)
    
    all_ok = True
    
    # 1. 检查配置文件
    print("\n📋 配置文件检查：")
    print("-" * 60)
    all_ok &= check_file_exists("runtime.txt", "Python版本定义")
    all_ok &= check_file_exists("requirements.txt", "项目依赖")
    all_ok &= check_file_exists("koyeb.yml", "Koyeb构建配置")
    all_ok &= check_file_exists(".koyeb-deploy.yaml", "GPU部署配置")
    all_ok &= check_file_exists("webui.py", "应用入口点")
    all_ok &= check_file_exists(".gitignore", "Git忽略配置")
    
    # 2. 检查runtime.txt内容
    print("\n📦 Python版本检查：")
    print("-" * 60)
    all_ok &= check_file_content("runtime.txt", "python-3.10.13", "Python版本指定为3.10.13")
    
    # 3. 检查requirements.txt内容
    print("\n📚 依赖包检查：")
    print("-" * 60)
    required_packages = [
        "gradio",
        "transformers",
        "spaces",
        "librosa",
        "numpy",
        "accelerate",
    ]
    
    try:
        with open("requirements.txt", 'r') as f:
            req_content = f.read()
            for pkg in required_packages:
                if pkg in req_content:
                    print(f"✅ 依赖 '{pkg}' 已包含")
                else:
                    print(f"⚠️  依赖 '{pkg}' 未找到")
                    all_ok = False
    except Exception as e:
        print(f"❌ 检查requirements.txt失败：{e}")
        all_ok = False
    
    # 4. 检查koyeb.yml
    print("\n🚀 Koyeb配置检查：")
    print("-" * 60)
    all_ok &= check_file_content("koyeb.yml", "buildpack: python", "构建器类型为Python")
    all_ok &= check_file_content("koyeb.yml", "3.10.13", "Python版本已配置")
    all_ok &= check_file_content("koyeb.yml", "webui.py", "应用入口点已配置")
    
    # 5. 检查GPU配置
    print("\n🎮 GPU配置检查：")
    print("-" * 60)
    all_ok &= check_file_content(".koyeb-deploy.yaml", "a4000", "GPU类型为A4000")
    all_ok &= check_file_content(".koyeb-deploy.yaml", "koyeb-deploy-gpu-a4000-github-define-python", "正确的分支")
    
    # 6. 检查webui.py
    print("\n🔧 应用配置检查：")
    print("-" * 60)
    all_ok &= check_file_content("webui.py", "cmd_args.port", "支持端口参数")
    all_ok &= check_file_content("webui.py", "cmd_args.host", "支持主机参数")
    all_ok &= check_file_content("webui.py", "demo.launch", "Gradio启动配置")
    
    # 7. 文件计数
    print("\n📊 文件统计：")
    print("-" * 60)
    try:
        with open("requirements.txt", 'r') as f:
            num_packages = len([line for line in f if line.strip() and not line.startswith('#')])
        print(f"✅ requirements.txt 包含 {num_packages} 个包")
    except:
        print("⚠️  无法统计requirements.txt")
    
    # 最终结果
    print("\n" + "=" * 60)
    if all_ok:
        print("✅ 所有配置检查通过！")
        print("\n🎉 项目已准备好部署到Koyeb!")
        print("\n部署步骤：")
        print("1. 打开 https://app.koyeb.com")
        print("2. 选择 GitHub 仓库")
        print("3. 选择分支 'koyeb-deploy-gpu-a4000-github-define-python'")
        print("4. 配置：Python 3.10.13 + A4000 GPU")
        print("5. 点击部署")
        return 0
    else:
        print("⚠️  部分配置有问题，请检查上面的错误")
        return 1

if __name__ == "__main__":
    sys.exit(main())
