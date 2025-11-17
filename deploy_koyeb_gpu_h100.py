#!/usr/bin/env python3

"""
Koyeb GPU H100 部署脚本 (Python版本)
根据Koyeb官方文档: https://www.koyeb.com/docs
使用Python部署带GPU（H100）的容器
"""

import json
import os
import sys
import argparse
import requests
from typing import Dict, Any, Optional
from urllib.parse import urljoin
from datetime import datetime


class KoyebDeployer:
    """Koyeb部署器"""

    def __init__(self, api_key: str, api_url: str = "https://app.koyeb.com/v1"):
        """
        初始化部署器
        
        Args:
            api_key: Koyeb API密钥
            api_url: Koyeb API基础URL
        """
        self.api_key = api_key
        self.api_url = api_url
        self.session = self._create_session()

    def _create_session(self) -> requests.Session:
        """创建请求会话"""
        session = requests.Session()
        session.headers.update({
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
            'User-Agent': 'IndexTTS-Koyeb-Deployer/1.0'
        })
        return session

    def create_deployment_config(
        self,
        name: str,
        instance_type: str = "gpu-h100",
        container_port: int = 7860,
        memory: str = "16Gi",
        cpu: str = "8",
        git_repo: Optional[str] = None,
        git_branch: str = "main",
        docker_image: Optional[str] = None,
        env: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        创建部署配置
        
        Args:
            name: 部署名称
            instance_type: 实例类型（如 gpu-h100）
            container_port: 容器端口
            memory: 内存大小
            cpu: CPU核心数
            git_repo: Git仓库URL
            git_branch: Git分支
            docker_image: Docker镜像（如果使用镜像而不是Git）
            env: 环境变量字典
            
        Returns:
            部署配置字典
        """
        config: Dict[str, Any] = {
            "displayName": name,
            "name": name,
            "instance": {
                "type": instance_type
            },
            "deployment": {
                "containerPort": container_port,
                "resources": {
                    "memory": memory,
                    "cpu": cpu
                },
                "ports": [
                    {
                        "port": container_port,
                        "protocol": "http"
                    }
                ],
                "env": [
                    {
                        "key": "GRADIO_SERVER_NAME",
                        "value": "0.0.0.0"
                    },
                    {
                        "key": "GRADIO_SERVER_PORT",
                        "value": str(container_port)
                    }
                ]
            }
        }

        # 添加自定义环境变量
        if env:
            for key, value in env.items():
                config["deployment"]["env"].append({
                    "key": key,
                    "value": str(value)
                })

        # 配置Docker或Git源
        if docker_image:
            config["deployment"]["docker"] = {
                "image": docker_image,
                "entrypoint": []
            }
        elif git_repo:
            config["git"] = {
                "repository": git_repo,
                "branch": git_branch
            }
            config["deployment"]["docker"] = {
                "command": [
                    "python",
                    "webui.py",
                    "--host",
                    "0.0.0.0",
                    "--port",
                    str(container_port)
                ],
                "dockerfile": "Dockerfile",
                "entrypoint": []
            }
        else:
            raise ValueError("必须提供 git_repo 或 docker_image")

        return config

    def deploy(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行部署
        
        Args:
            config: 部署配置
            
        Returns:
            API响应
        """
        try:
            print("📤 发送部署请求到Koyeb...")
            response = self.session.post(
                urljoin(self.api_url, '/deployments'),
                json=config
            )
            response.raise_for_status()

            result = response.json()
            print("✅ 部署成功！")
            return result

        except requests.exceptions.RequestException as e:
            print(f"❌ 部署失败: {e}")
            if hasattr(e.response, 'text'):
                print(f"响应: {e.response.text}")
            raise

    def get_deployment_status(self, deployment_id: str) -> Dict[str, Any]:
        """
        获取部署状态
        
        Args:
            deployment_id: 部署ID
            
        Returns:
            部署信息
        """
        try:
            print(f"⏳ 获取部署状态 (ID: {deployment_id})...")
            response = self.session.get(
                urljoin(self.api_url, f'/deployments/{deployment_id}')
            )
            response.raise_for_status()

            result = response.json()
            print("✅ 获取成功！")
            return result

        except requests.exceptions.RequestException as e:
            print(f"❌ 获取失败: {e}")
            if hasattr(e.response, 'text'):
                print(f"响应: {e.response.text}")
            raise

    def list_deployments(self) -> Dict[str, Any]:
        """
        列出所有部署
        
        Returns:
            部署列表
        """
        try:
            print("⏳ 获取部署列表...")
            response = self.session.get(
                urljoin(self.api_url, '/deployments')
            )
            response.raise_for_status()

            result = response.json()
            print("✅ 获取成功！")
            return result

        except requests.exceptions.RequestException as e:
            print(f"❌ 获取失败: {e}")
            if hasattr(e.response, 'text'):
                print(f"响应: {e.response.text}")
            raise

    def delete_deployment(self, deployment_id: str) -> bool:
        """
        删除部署
        
        Args:
            deployment_id: 部署ID
            
        Returns:
            是否成功
        """
        try:
            print(f"🗑️  删除部署 (ID: {deployment_id})...")
            response = self.session.delete(
                urljoin(self.api_url, f'/deployments/{deployment_id}')
            )
            response.raise_for_status()

            print("✅ 删除成功！")
            return True

        except requests.exceptions.RequestException as e:
            print(f"❌ 删除失败: {e}")
            if hasattr(e.response, 'text'):
                print(f"响应: {e.response.text}")
            raise

    def wait_for_deployment(self, deployment_id: str, max_attempts: int = 60, interval: int = 10) -> bool:
        """
        等待部署完成
        
        Args:
            deployment_id: 部署ID
            max_attempts: 最大尝试次数
            interval: 检查间隔（秒）
            
        Returns:
            部署是否成功
        """
        import time

        for attempt in range(max_attempts):
            try:
                status = self.get_deployment_status(deployment_id)
                deployment_status = status.get('status', 'unknown')

                print(f"[{datetime.now().strftime('%H:%M:%S')}] 部署状态: {deployment_status}")

                if deployment_status == 'active':
                    print("🎉 部署已激活！")
                    return True
                elif deployment_status == 'error':
                    print("❌ 部署出错！")
                    return False

                if attempt < max_attempts - 1:
                    print(f"⏳ {interval}秒后重试...")
                    time.sleep(interval)

            except Exception as e:
                print(f"⚠️  检查状态出错: {e}")
                if attempt < max_attempts - 1:
                    time.sleep(interval)

        print(f"⏱️  达到最大尝试次数 ({max_attempts})")
        return False


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="Koyeb GPU H100 部署工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 从Git部署
  %(prog)s deploy --git-repo https://github.com/user/indextts --git-branch main
  
  # 从Docker镜像部署
  %(prog)s deploy --docker-image user/indextts:latest
  
  # 检查部署状态
  %(prog)s status <deployment-id>
  
  # 列出所有部署
  %(prog)s list
  
  # 删除部署
  %(prog)s delete <deployment-id>
        """
    )

    # 全局参数
    parser.add_argument(
        '--api-key',
        type=str,
        default=os.getenv('KOYEB_API_KEY'),
        help='Koyeb API密钥 (默认: 从KOYEB_API_KEY环境变量读取)'
    )
    parser.add_argument(
        '--api-url',
        type=str,
        default='https://app.koyeb.com/v1',
        help='Koyeb API URL (默认: https://app.koyeb.com/v1)'
    )

    subparsers = parser.add_subparsers(dest='command', help='命令')

    # deploy 子命令
    deploy_parser = subparsers.add_parser('deploy', help='部署应用')
    deploy_parser.add_argument('--name', type=str, default='indextts-gpu-h100', help='部署名称')
    deploy_parser.add_argument('--instance-type', type=str, default='gpu-h100', help='实例类型')
    deploy_parser.add_argument('--container-port', type=int, default=7860, help='容器端口')
    deploy_parser.add_argument('--memory', type=str, default='16Gi', help='内存大小')
    deploy_parser.add_argument('--cpu', type=str, default='8', help='CPU核心数')
    deploy_parser.add_argument('--git-repo', type=str, help='Git仓库URL')
    deploy_parser.add_argument('--git-branch', type=str, default='main', help='Git分支')
    deploy_parser.add_argument('--docker-image', type=str, help='Docker镜像')
    deploy_parser.add_argument('--wait', action='store_true', help='等待部署完成')

    # status 子命令
    status_parser = subparsers.add_parser('status', help='获取部署状态')
    status_parser.add_argument('deployment_id', type=str, help='部署ID')

    # list 子命令
    list_parser = subparsers.add_parser('list', help='列出所有部署')

    # delete 子命令
    delete_parser = subparsers.add_parser('delete', help='删除部署')
    delete_parser.add_argument('deployment_id', type=str, help='部署ID')

    args = parser.parse_args()

    # 验证API密钥
    if not args.api_key:
        print("❌ 错误: 未提供API密钥")
        print("请设置 KOYEB_API_KEY 环境变量或使用 --api-key 选项")
        sys.exit(1)

    # 创建部署器
    deployer = KoyebDeployer(args.api_key, args.api_url)

    try:
        if args.command == 'deploy':
            # 部署
            print("🚀 开始部署IndexTTS到Koyeb（GPU H100）...")
            print(f"📦 部署名称: {args.name}")
            print(f"🎮 实例类型: {args.instance_type}")
            print(f"💾 内存: {args.memory}")
            print(f"⚙️  CPU: {args.cpu}")
            print()

            # 创建配置
            config = deployer.create_deployment_config(
                name=args.name,
                instance_type=args.instance_type,
                container_port=args.container_port,
                memory=args.memory,
                cpu=args.cpu,
                git_repo=args.git_repo,
                git_branch=args.git_branch,
                docker_image=args.docker_image
            )

            print("📋 部署配置:")
            print(json.dumps(config, indent=2, ensure_ascii=False))
            print()

            # 执行部署
            result = deployer.deploy(config)
            print()
            print("📊 部署结果:")
            print(json.dumps(result, indent=2, ensure_ascii=False))

            deployment_id = result.get('id')
            if deployment_id:
                print()
                print(f"📍 部署ID: {deployment_id}")
                print(f"🔗 查看部署: {args.api_url}/deployments/{deployment_id}")

                if args.wait:
                    print()
                    deployer.wait_for_deployment(deployment_id)

        elif args.command == 'status':
            # 获取状态
            result = deployer.get_deployment_status(args.deployment_id)
            print()
            print("📊 部署状态:")
            print(json.dumps(result, indent=2, ensure_ascii=False))

        elif args.command == 'list':
            # 列出部署
            result = deployer.list_deployments()
            print()
            print("📊 部署列表:")
            print(json.dumps(result, indent=2, ensure_ascii=False))

        elif args.command == 'delete':
            # 删除部署
            deployer.delete_deployment(args.deployment_id)

        else:
            parser.print_help()

    except KeyboardInterrupt:
        print("\n⚠️  操作被中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
