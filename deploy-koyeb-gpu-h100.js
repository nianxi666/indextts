#!/usr/bin/env node

/**
 * Koyeb GPU H100 部署脚本 (JavaScript/Node.js版本)
 * 根据Koyeb官方文档: https://www.koyeb.com/docs
 * 使用JavaScript部署带GPU（H100）的容器
 */

const https = require('https');
const http = require('http');

// 配置信息
const config = {
    apiKey: 'd5yqxgmxn08waujluulb2iczhsfi4kic1lfob7rs1skim4h2jajyxkiospyuxjex',
    apiUrl: 'https://app.koyeb.com/v1',
    deploymentName: 'indextts-gpu-h100',
    containerPort: 7860,
    instanceType: 'gpu-h100', // H100 GPU实例类型
    memory: '16Gi',
    cpu: '8',
    // 如果使用镜像仓库，设置以下信息
    dockerImage: 'your-org/indextts:latest',
    gitRepository: 'https://github.com/your-org/indextts',
    gitBranch: 'main'
};

/**
 * 发送HTTP请求
 */
function makeRequest(method, path, data = null) {
    return new Promise((resolve, reject) => {
        const url = new URL(config.apiUrl + path);
        const isHttps = url.protocol === 'https:';
        const client = isHttps ? https : http;

        const options = {
            hostname: url.hostname,
            port: url.port,
            path: url.pathname + url.search,
            method: method,
            headers: {
                'Authorization': `Bearer ${config.apiKey}`,
                'Content-Type': 'application/json'
            }
        };

        if (data) {
            options.headers['Content-Length'] = Buffer.byteLength(data);
        }

        const req = client.request(options, (res) => {
            let responseData = '';

            res.on('data', (chunk) => {
                responseData += chunk;
            });

            res.on('end', () => {
                try {
                    const parsed = JSON.parse(responseData);
                    resolve({
                        status: res.statusCode,
                        data: parsed
                    });
                } catch (e) {
                    resolve({
                        status: res.statusCode,
                        data: responseData
                    });
                }
            });
        });

        req.on('error', (err) => {
            reject(err);
        });

        if (data) {
            req.write(data);
        }

        req.end();
    });
}

/**
 * 创建部署配置
 */
function createDeploymentConfig() {
    const deploymentConfig = {
        displayName: config.deploymentName,
        deployment: {
            containerPort: config.containerPort,
            docker: {
                command: [
                    'python',
                    'webui.py',
                    '--host',
                    '0.0.0.0',
                    '--port',
                    String(config.containerPort)
                ],
                dockerfile: 'Dockerfile',
                entrypoint: []
            },
            env: [
                {
                    key: 'GRADIO_SERVER_NAME',
                    value: '0.0.0.0'
                },
                {
                    key: 'GRADIO_SERVER_PORT',
                    value: String(config.containerPort)
                },
                {
                    key: 'HF_TOKEN',
                    value: process.env.HF_TOKEN || ''
                }
            ],
            resources: {
                memory: config.memory,
                cpu: config.cpu
            },
            ports: [
                {
                    port: config.containerPort,
                    protocol: 'http'
                }
            ]
        },
        git: {
            branch: config.gitBranch,
            repository: config.gitRepository
        },
        instance: {
            type: config.instanceType
        },
        name: config.deploymentName
    };

    return deploymentConfig;
}

/**
 * 部署到Koyeb
 */
async function deployToKoyeb() {
    try {
        console.log('🚀 开始部署IndexTTS到Koyeb（GPU H100）...');
        console.log(`📦 部署名称: ${config.deploymentName}`);
        console.log(`🎮 实例类型: ${config.instanceType}`);
        console.log(`💾 内存: ${config.memory}`);
        console.log(`⚙️  CPU: ${config.cpu}`);
        console.log('');

        const deploymentConfig = createDeploymentConfig();

        console.log('📋 部署配置:');
        console.log(JSON.stringify(deploymentConfig, null, 2));
        console.log('');

        console.log('⏳ 向Koyeb API发送部署请求...');
        const response = await makeRequest(
            'POST',
            '/deployments',
            JSON.stringify(deploymentConfig)
        );

        if (response.status >= 200 && response.status < 300) {
            console.log('✅ 部署成功！');
            console.log('');
            console.log('📊 部署信息:');
            console.log(JSON.stringify(response.data, null, 2));

            if (response.data.id) {
                console.log('');
                console.log(`📍 部署ID: ${response.data.id}`);
                console.log(`🌐 查看部署状态: ${config.apiUrl}/deployments/${response.data.id}`);
            }

            return response.data;
        } else {
            console.error('❌ 部署失败！');
            console.error(`状态码: ${response.status}`);
            console.error('响应:', JSON.stringify(response.data, null, 2));
            process.exit(1);
        }
    } catch (error) {
        console.error('❌ 部署出错:', error.message);
        process.exit(1);
    }
}

/**
 * 获取部署状态
 */
async function getDeploymentStatus(deploymentId) {
    try {
        console.log(`⏳ 获取部署状态 (ID: ${deploymentId})...`);

        const response = await makeRequest(
            'GET',
            `/deployments/${deploymentId}`
        );

        if (response.status >= 200 && response.status < 300) {
            console.log('✅ 获取成功！');
            console.log('');
            console.log('📊 部署状态信息:');
            console.log(JSON.stringify(response.data, null, 2));
            return response.data;
        } else {
            console.error('❌ 获取失败！');
            console.error(`状态码: ${response.status}`);
            console.error('响应:', JSON.stringify(response.data, null, 2));
            process.exit(1);
        }
    } catch (error) {
        console.error('❌ 获取部署状态出错:', error.message);
        process.exit(1);
    }
}

/**
 * 列出所有部署
 */
async function listDeployments() {
    try {
        console.log('⏳ 获取部署列表...');

        const response = await makeRequest('GET', '/deployments');

        if (response.status >= 200 && response.status < 300) {
            console.log('✅ 获取成功！');
            console.log('');
            console.log('📊 部署列表:');
            console.log(JSON.stringify(response.data, null, 2));
            return response.data;
        } else {
            console.error('❌ 获取失败！');
            console.error(`状态码: ${response.status}`);
            console.error('响应:', JSON.stringify(response.data, null, 2));
            process.exit(1);
        }
    } catch (error) {
        console.error('❌ 获取部署列表出错:', error.message);
        process.exit(1);
    }
}

/**
 * 主函数
 */
async function main() {
    const args = process.argv.slice(2);

    if (args.length === 0) {
        // 执行部署
        await deployToKoyeb();
    } else {
        const command = args[0];

        if (command === 'status' && args[1]) {
            // 获取部署状态
            await getDeploymentStatus(args[1]);
        } else if (command === 'list') {
            // 列出所有部署
            await listDeployments();
        } else {
            console.error('❌ 未知命令！');
            console.log('');
            console.log('用法:');
            console.log('  node deploy-koyeb-gpu-h100.js          # 部署应用');
            console.log('  node deploy-koyeb-gpu-h100.js status <deployment-id>  # 获取部署状态');
            console.log('  node deploy-koyeb-gpu-h100.js list     # 列出所有部署');
            process.exit(1);
        }
    }
}

// 运行主函数
if (require.main === module) {
    main();
}

module.exports = {
    deployToKoyeb,
    getDeploymentStatus,
    listDeployments,
    makeRequest,
    config
};
