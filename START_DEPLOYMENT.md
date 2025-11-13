# 🚀 开始部署 - IndexTTS WebUI到Koyeb

## 📌 关键信息

**当前分支**: `koyeb-deploy-gpu-a4000-github-define-python`  
**状态**: ✅ 所有配置已完成  
**下一步**: 提交代码 → 推送到GitHub → 在Koyeb中部署

---

## 第1步：提交和推送代码

在您的项目目录中运行以下命令：

```bash
# 进入项目目录
cd /home/engine/project

# 查看要提交的文件
git status

# 添加所有新创建的Koyeb配置文件
git add .

# 提交
git commit -m "feat: Add Koyeb deployment configuration for GPU A4000 deployment with Python 3.10.13"

# 推送到部署分支
git push origin koyeb-deploy-gpu-a4000-github-define-python
```

**✅ 确认**：确保最后一条push命令执行成功，没有错误。

---

## 第2步：在Koyeb中创建服务

### 2.1 打开Koyeb控制面板
- 访问 https://app.koyeb.com
- 使用您的账户登录（如果没有账户，先注册）

### 2.2 创建新服务
1. 点击 **"Create Service"** 按钮
2. 在弹出的选项中选择 **"GitHub"**
3. 授权Koyeb访问您的GitHub账户（如果需要）

### 2.3 选择仓库和分支
1. 在"Repository"部分找到您的仓库
2. 选择仓库
3. **重要⚠️**: 在"Branch"下拉菜单中选择 **`koyeb-deploy-gpu-a4000-github-define-python`**
   - 不要选择main或其他分支！
   - 只有这个分支有完整的GPU配置

### 2.4 配置构建器（Builder）

在"Build"部分配置：
- **Builder Type**: Buildpack
- **Buildpack**: Python
- **Python Version**: 3.10.13
  - 确保明确指定此版本，即使有默认值

### 2.5 配置运行命令

在"Run Command"字段输入：
```bash
python webui.py --host 0.0.0.0 --port $PORT
```

**说明**: 
- `--host 0.0.0.0` 允许外部访问
- `--port $PORT` 使用Koyeb提供的端口

### 2.6 配置资源（Resources）

这是部署成功的关键配置：

#### 实例类型
- **Instance Type**: GPU Instance
- **GPU Type**: NVIDIA A4000 (重要!)
- **vCPU**: 4
- **Memory**: 16Gi (16GB)

#### 端口配置
- **Port**: 7860
- **Protocol**: HTTP
- **Public**: 启用（打钩）

### 2.7 添加环境变量

点击 "Environment Variables" 添加以下变量：

| 变量名 | 值 |
|--------|-----|
| GRADIO_SHARE | false |
| HF_HOME | /workspace/.huggingface |
| TRANSFORMERS_CACHE | /workspace/.cache/transformers |

**说明**：
- `GRADIO_SHARE=false`: 不使用Gradio公共分享，而是使用Koyeb提供的URL
- 其他两个变量用于缓存Hugging Face模型

### 2.8 配置其他选项（可选）

#### 服务名称
- 设置一个有意义的名字，例如：`indextts-webui`

#### 扩展选项
- **Min Replicas**: 1
- **Max Replicas**: 1（除非需要扩展）

### 2.9 开始部署

1. 检查所有配置是否正确
2. 点击 **"Deploy"** 按钮
3. Koyeb开始构建和部署

---

## 第3步：监控部署进度

### 查看部署日志

1. 部署开始后，Koyeb会显示实时日志
2. 查看构建进度：
   - 依赖安装进度
   - 错误或警告信息

### 预期过程

部署应该经过以下阶段：

```
1. 🔨 构建阶段（2-5分钟）
   - 设置Python环境
   - 安装依赖包

2. 📦 依赖安装（5-15分钟）
   - 安装31个Python包
   - 编译必要的C扩展（如Cython）

3. 🚀 启动应用（2-5分钟）
   - 运行webui.py
   - 初始化Gradio界面
   - 首次下载模型权重（5-15分钟）

4. ✅ 完成
   - 应用已部署并运行
   - 获得公开URL
```

**总耗时**: 约20-40分钟

### 如果部署失败

1. **检查日志**：查看错误信息
2. **常见问题**：
   - 依赖安装错误 → 检查Python版本和requirements.txt
   - GPU不可用 → 确认A4000是否可用
   - 内存不足 → 增加内存配置
3. **重新部署**：修复问题后，点击"Redeploy"

---

## 第4步：访问应用

### 获取应用URL

1. 部署完成后，在Koyeb控制面板中查看服务详情
2. 找到 **"Koyeb URL"** 或 **"Public URL"** 部分
3. 复制提供的URL

### 打开应用

1. 在浏览器中粘贴URL
2. 等待应用加载（首次可能较慢）
3. 应该看到Gradio Web界面

### 测试功能

1. 上传或录制提示音频
2. 输入文本（中文或英文）
3. 选择情感控制方式
4. 点击生成
5. 等待语音生成完成

---

## ✅ 验证清单

| 项目 | 检查 |
|------|------|
| 分支正确 | ✓ koyeb-deploy-gpu-a4000-github-define-python |
| Python版本 | ✓ 3.10.13 |
| GPU类型 | ✓ NVIDIA A4000 |
| CPU和内存 | ✓ 4 vCPU, 16GB |
| 运行命令 | ✓ python webui.py --host 0.0.0.0 --port $PORT |
| 环境变量 | ✓ GRADIO_SHARE=false, HF_HOME, TRANSFORMERS_CACHE |
| requirements.txt | ✓ 包含所有依赖 |
| runtime.txt | ✓ 指定Python 3.10.13 |

---

## 🔄 更新应用

部署后，如果需要更新应用：

1. 在本地修改代码
2. 运行以下命令：
   ```bash
   git add .
   git commit -m "Update application"
   git push origin koyeb-deploy-gpu-a4000-github-define-python
   ```
3. Koyeb会自动检测到更新并重新部署

---

## 📊 成本提示

- **A4000 GPU**: 这是付费GPU，会产生成本
- **存储**: 模型缓存需要约2-5GB存储空间
- **网络**: 首次启动时从Hugging Face下载模型会产生网络成本

访问 [Koyeb定价页面](https://koyeb.com/pricing) 了解详细费用。

---

## 🆘 常见问题

### Q: 部署卡在某个步骤？
**A**: 
- 检查日志中的错误信息
- 确保GPU A4000可用
- 尝试增加内存或CPU
- 重新启动部署

### Q: 应用启动很慢？
**A**: 这是正常的。首次启动需要：
- 安装依赖（5-15分钟）
- 从Hugging Face下载模型（5-15分钟）
- 初始化TTS引擎（1-3分钟）

### Q: 如何查看实时日志？
**A**: 在Koyeb服务页面，点击 "Logs" 标签即可查看实时输出。

### Q: 如何重启服务？
**A**: 在Koyeb服务页面，点击 "Restart Service" 按钮。

### Q: 如何删除服务？
**A**: 在Koyeb服务页面，点击 "Delete Service" 按钮（需要确认）。

---

## 📞 获取帮助

- **Koyeb文档**: https://koyeb.com/docs
- **Koyeb支持**: https://koyeb.com/support
- **IndexTTS2**: https://github.com/InternLM/IndexTTS2
- **Gradio**: https://www.gradio.app/docs

---

## 🎯 总结

1. ✅ **配置完成** - 所有Koyeb配置文件已创建
2. ⏳ **第1步** - 提交和推送代码到分支
3. ⏳ **第2步** - 在Koyeb控制面板中配置和部署
4. ⏳ **第3步** - 监控部署进度
5. ⏳ **第4步** - 访问并使用应用

---

**准备开始了吗？** 现在就运行第1步的命令开始部署吧！🚀

---

**参考资料**:
- API令牌: rocrorea70dhiis0zw0u68j35xve4ljjpt6ytw2sz7ixbr8y70ox7dpgqj497h28
- 部署分支: koyeb-deploy-gpu-a4000-github-define-python
- 更多文档: 查看本仓库中的其他 .md 文件
