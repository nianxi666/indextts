# 🚀 立即部署到Koyeb - 完整指导

## ✅ 已准备就绪

- ✅ Python版本已正确定义（python-3.10）
- ✅ 所有配置文件已修正
- ✅ 代码已推送到GitHub分支
- ✅ 现在可以部署

---

## 📋 部署前最后确认

### 配置文件状态
```
✅ runtime.txt: python-3.10
✅ koyeb.yml: PYTHON_VERSION="3.10"
✅ .koyeb-deploy.yaml: 已更新
✅ requirements.txt: 31个依赖包
✅ README.md: 已更新
```

### 关键信息
- **分支**: koyeb-deploy-gpu-a4000-github-define-python
- **Python**: 3.10（正确定义）
- **GPU**: NVIDIA A4000
- **CPU**: 4核
- **内存**: 16GB
- **端口**: 7860

---

## 🌐 Koyeb部署步骤（10分钟）

### 第1步：登录Koyeb控制面板
1. 打开浏览器访问: **https://app.koyeb.com**
2. 使用您的Koyeb账户登录
   - 如果没有账户，点击 "Sign up" 注册
   - GitHub账户可直接登录

### 第2步：创建新服务
1. 点击左侧菜单 **"Services"**
2. 点击 **"Create Service"** 按钮
3. 在弹出的选项中选择 **"GitHub"**

### 第3步：连接GitHub
1. 如果首次使用，点击 "Connect your GitHub account"
2. 授权Koyeb访问您的GitHub仓库
3. 选择您的 `indextts` 仓库

### 第4步：选择分支和构建器
**重要**: 这一步很关键！

在 "GitHub" 部分配置：
- **Repository**: nianxi666/indextts （您的仓库）
- **Branch**: 👉 **koyeb-deploy-gpu-a4000-github-define-python** ⚠️ 必须选择这个分支！
- **Builder**: Buildpack （自动选中）

### 第5步：配置服务名称
1. 输入服务名称: `indextts-webui`
2. 或任何您喜欢的名称

### 第6步：配置构建和运行
在 "Build" 部分：
- 应该自动检测到 Python
- 如果需要，确认 `runtime.txt` 被检测到

在 "Run Command" 部分：
- 默认应该是: `python webui.py --host 0.0.0.0 --port $PORT`
- 如果为空，手动输入上述命令

### 第7步：配置环境变量
点击 "Environment Variables" 添加以下变量：

```
GRADIO_SHARE           false
HF_HOME                /workspace/.huggingface
TRANSFORMERS_CACHE     /workspace/.cache/transformers
```

### 第8步：配置资源和GPU
这是部署成功的关键！

找到 "Resources" 部分：

#### Instance Type
1. 点击 "Instance Type" 下拉菜单
2. 选择 **"GPU Instance"**

#### GPU配置
1. **GPU Type**: 选择 **"NVIDIA A4000"** ⚠️ 必须是A4000！
2. **vCPU**: 4
3. **Memory**: 16Gi
4. **Port**: 7860
   - 确保 "Publicly Exposed" 或 "Public" 已勾选

### 第9步：配置自动部署（可选）
如果想要在代码更新时自动重新部署：
- 启用 "Auto-deploy on push" （如果有此选项）

### 第10步：开始部署
1. 检查所有配置是否正确
2. 点击底部的 **"Deploy"** 按钮
3. 等待部署开始

---

## ⏱️ 部署进度监控

### 部署开始后的流程

1. **构建开始** (1-2分钟)
   - Koyeb开始克隆仓库
   - 检测到 Python buildpack

2. **依赖安装** (5-15分钟)
   - 安装所有requirements.txt中的包
   - 这可能需要较长时间

3. **模型下载** (5-15分钟)
   - webui.py启动时会自动下载模型
   - 这是正常的，需要耐心等待

4. **应用启动** (1-5分钟)
   - Gradio应用初始化
   - 准备处理请求

5. **部署完成** ✅
   - 会看到 "Active" 状态
   - Koyeb提供的URL变为可访问

### 查看日志
部署过程中查看日志：
1. 在服务页面找到 "Logs" 标签
2. 实时查看构建和启动日志
3. 如果有错误，错误信息会显示在这里

### 如果部署失败
1. 查看日志了解具体错误
2. 常见问题：
   - 分支选择错误 → 重新创建服务
   - GPU不可用 → 联系Koyeb支持或选择其他GPU
   - 内存不足 → 增加内存配置
   - 依赖安装失败 → 检查requirements.txt兼容性

---

## 🎯 部署完成后

### 1. 获取应用URL
部署完成后：
1. 在服务页面找到 "URL" 或 "Domain"
2. 会看到类似 `https://indextts-webui-xxxxx.koyeb.app` 的URL
3. 复制此URL

### 2. 访问应用
1. 打开浏览器
2. 粘贴URL
3. 等待Gradio界面加载（首次可能较慢，因为要初始化模型）

### 3. 测试功能
1. 上传或录制提示音频
2. 输入要转换的文本（中文或英文）
3. 选择情感控制方式
4. 点击 "Generate" 或"生成"
5. 等待语音生成完成

### 4. 分享URL
- URL可以分享给他人使用
- 无需额外配置，直接访问即可

---

## 📊 部署预期时间

| 阶段 | 时间 |
|------|------|
| GitHub连接 | 1-2分钟 |
| 构建环境 | 2-5分钟 |
| 依赖安装 | 5-15分钟 |
| 模型下载 | 5-15分钟 |
| 应用启动 | 1-5分钟 |
| **总计** | **15-45分钟** |

**后续启动**: 2-5分钟（模型已缓存）

---

## 🔑 关键提示

### 分支选择
⚠️ **最重要**: 必须选择分支 `koyeb-deploy-gpu-a4000-github-define-python`
- 这是包含所有GPU配置的分支
- 如果选错分支，GPU配置会被忽略

### GPU选择
⚠️ **A4000是付费GPU**
- 查看费用: https://koyeb.com/pricing
- 确保了解成本

### 等待时间
⏱️ **首次启动需要20-45分钟**
- 这是正常的，主要是下载模型
- 不要中断部署过程

### 环境变量
✓ **三个环境变量很重要**
- GRADIO_SHARE: 使用Koyeb提供的URL而不是公共分享
- HF_HOME和TRANSFORMERS_CACHE: 为模型设置缓存路径

---

## 🆘 常见问题快速解决

### Q: 分支选不到？
**A**: 
1. 确保已连接GitHub账户
2. 确保 `koyeb-deploy-gpu-a4000-github-define-python` 分支已推送到GitHub
3. 刷新页面重试

### Q: 找不到A4000 GPU？
**A**:
1. 确认 Instance Type 选择了 "GPU Instance"
2. 确保您的Koyeb账户有GPU配额
3. 尝试先部署不带GPU，然后升级资源

### Q: 部署卡在某个阶段？
**A**:
1. 查看日志了解进度
2. 通常在安装依赖或下载模型时需要等待
3. 不要立即重新部署，等待至少30分钟

### Q: 应用无法访问？
**A**:
1. 确保服务状态是 "Active"
2. 检查端口是否设置为 7860 且已暴露
3. 等待应用完全启动
4. 查看日志是否有错误

### Q: 端口错误或超时？
**A**:
1. 确认运行命令中使用了 `$PORT` 变量
2. 不要硬编码 7860，必须使用 `$PORT`
3. 重新创建服务

---

## 💻 部署检查清单

在点击 "Deploy" 前检查：

- [ ] 分支: `koyeb-deploy-gpu-a4000-github-define-python` ✓
- [ ] Python: 3.10（通过runtime.txt） ✓
- [ ] 运行命令: `python webui.py --host 0.0.0.0 --port $PORT` ✓
- [ ] GPU: NVIDIA A4000 ✓
- [ ] vCPU: 4 ✓
- [ ] 内存: 16Gi ✓
- [ ] 端口: 7860 (public) ✓
- [ ] 环境变量: 3个已添加 ✓

**所有检查通过后，点击 Deploy！**

---

## 📞 部署过程中需要帮助？

### Koyeb官方资源
- **文档**: https://koyeb.com/docs
- **部署指南**: https://koyeb.com/docs/deploy/github
- **Python指南**: https://koyeb.com/docs/build-and-deploy/build-from-git/python
- **支持**: https://koyeb.com/support

### 项目资源
- **GitHub**: https://github.com/nianxi666/indextts
- **部署分支**: koyeb-deploy-gpu-a4000-github-define-python

---

## 🎉 准备好了吗？

所有配置都正确无误，现在就可以部署了！

**立即前往**: https://app.koyeb.com

**步骤**: 按照上面的第1-10步操作

**预期**: 20-45分钟后应用上线

**记住**: 
✅ 选择正确的分支
✅ 选择A4000 GPU
✅ 添加环境变量
✅ 使用 $PORT 变量

---

**现在开始部署！🚀**
