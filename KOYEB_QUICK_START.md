# Koyeb快速部署指南（中文）

## 📦 已准备好的配置文件

部署所需的所有文件已全部配置：

| 文件名 | 用途 | 状态 |
|--------|------|------|
| `runtime.txt` | 定义Python版本（3.10.13） | ✅ |
| `requirements.txt` | 项目依赖 | ✅ |
| `koyeb.yml` | Koyeb构建配置 | ✅ |
| `.koyeb-deploy.yaml` | GPU部署配置（A4000） | ✅ |
| `.gitignore` | Git忽略文件 | ✅ |
| `webui.py` | 应用入口点 | ✅ |

## 🚀 部署步骤（5分钟快速部署）

### 第1步：访问Koyeb控制面板
1. 打开 https://app.koyeb.com
2. 登录您的Koyeb账户
3. 如果没有账户，先注册一个

### 第2步：创建新服务
1. 点击 **"Create Service"** 或 **"创建服务"**
2. 在弹出窗口中选择 **"GitHub"**
3. 授权Koyeb访问您的GitHub账户

### 第3步：配置仓库和分支
1. 选择您的GitHub仓库
2. **重要**：选择分支 **`koyeb-deploy-gpu-a4000-github-define-python`**
3. 点击继续

### 第4步：配置构建设置
| 设置项 | 值 |
|--------|-----|
| **构建器类型** | Buildpack |
| **编程语言** | Python |
| **Python版本** | 3.10.13 |
| **运行命令** | `python webui.py --host 0.0.0.0 --port $PORT` |

### 第5步：配置资源
| 资源 | 值 |
|------|-----|
| **GPU** | NVIDIA A4000 |
| **vCPU** | 4 |
| **内存** | 16GB |
| **端口** | 7860 |

### 第6步：设置环境变量
添加以下环境变量：

```
GRADIO_SHARE=false
HF_HOME=/workspace/.huggingface
TRANSFORMERS_CACHE=/workspace/.cache/transformers
```

### 第7步：部署
1. 检查所有设置无误
2. 点击 **"Deploy"** 按钮
3. 等待部署完成（约20-40分钟）

## ✅ 验证部署

部署完成后：

1. 查看服务URL：Koyeb会为您分配一个公开URL
2. 访问URL：在浏览器中打开分配的URL
3. 等待应用加载：首次加载可能需要几分钟

## 🔑 重要信息

| 项目 | 值 |
|------|-----|
| **部署分支** | `koyeb-deploy-gpu-a4000-github-define-python` |
| **Python版本** | 3.10.13 |
| **GPU类型** | NVIDIA A4000 |
| **入口点** | webui.py |
| **Web框架** | Gradio |
| **API令牌** | rocrorea70dhiis0zw0u68j35xve4ljjpt6ytw2sz7ixbr8y70ox7dpgqj497h28 |

## ⏱️ 预期时间

- 第一次构建：10-20分钟（安装依赖）
- 模型下载：5-15分钟（首次）
- 应用启动：2-5分钟
- **总计**：约20-40分钟

## 🔄 自动更新

此分支上的任何推送都会自动触发重新部署：

```bash
# 推送代码更新时
git push origin koyeb-deploy-gpu-a4000-github-define-python

# Koyeb会自动检测到变化并重新部署
```

## 📊 配置详情

### Python环境
```
Python版本：3.10.13
包管理器：pip
依赖文件：requirements.txt
依赖数量：31个包 + 平台特定包
```

### 应用配置
```
框架：Gradio
主机：0.0.0.0
端口：7860
TTS引擎：IndexTTS2
支持语言：中文、英文
```

### 硬件配置
```
GPU：NVIDIA A4000
vCPU：4核
内存：16GB
存储：Koyeb默认存储
```

## 🆘 常见问题

### Q：为什么需要A4000 GPU？
**A：** IndexTTS2 TTS引擎需要GPU进行加速，A4000提供良好的性能-成本平衡。

### Q：首次启动很慢？
**A：** 这是正常的。首次启动需要下载模型检查点（数百MB到GB），后续启动会更快。

### Q：如何查看日志？
**A：** 在Koyeb服务详情页面，点击 **"Logs"** 标签查看实时日志。

### Q：如何更新代码？
**A：** 在分支 `koyeb-deploy-gpu-a4000-github-define-python` 上推送更新，Koyeb会自动重新部署。

### Q：如何停止/重启服务？
**A：** 在Koyeb服务详情页面进行操作：
- 停止：点击 **"Stop Service"**
- 重启：点击 **"Restart Service"**
- 删除：点击 **"Delete Service"**

## 📱 API令牌保管

您的Koyeb API令牌：
```
rocrorea70dhiis0zw0u68j35xve4ljjpt6ytw2sz7ixbr8y70ox7dpgqj497h28
```

**安全提示**：
- 不要在代码中硬编码令牌
- 不要公开分享令牌
- 保管好这个令牌用于CLI操作

## 📚 参考资源

- [Koyeb官方文档](https://koyeb.com/docs)
- [Koyeb GitHub部署指南](https://koyeb.com/docs/deploy/github)
- [IndexTTS2项目](https://github.com/InternLM/IndexTTS2)
- [Gradio文档](https://www.gradio.app)

## 🎯 下一步

1. ✅ 确认所有配置文件已创建
2. ✅ 代码已推送到分支 `koyeb-deploy-gpu-a4000-github-define-python`
3. ⏳ 访问Koyeb控制面板开始部署
4. ⏳ 等待部署完成并测试应用

---

**准备好部署了！** 🎉
