# 🚀 NOW - 立即部署到Koyeb

## ✅ 配置已全部修正

所有文件都已用**正确的Python版本定义**进行更新！

```
✅ runtime.txt: python-3.10 (已修正)
✅ koyeb.yml: PYTHON_VERSION="3.10" (已修正)
✅ 代码已推送到GitHub分支
✅ 准备部署！
```

---

## 🚀 部署方式（选一种）

### 方法1：手动通过Web UI部署（推荐新手）

#### 第1步：打开Koyeb
访问: **https://app.koyeb.com**

#### 第2步：创建服务
1. 点击左菜单 **"Services"** 
2. 点击 **"Create Service"**
3. 选择 **"GitHub"**

#### 第3步：配置
1. **Repository**: nianxi666/indextts
2. **Branch**: `koyeb-deploy-gpu-a4000-github-define-python` ⚠️ **必选此分支**
3. **Service Name**: indextts-webui

#### 第4步：构建配置
- 构建器自动检测为Python
- 运行命令: `python webui.py --host 0.0.0.0 --port $PORT`

#### 第5步：环境变量
添加三个变量：
```
GRADIO_SHARE = false
HF_HOME = /workspace/.huggingface
TRANSFORMERS_CACHE = /workspace/.cache/transformers
```

#### 第6步：资源配置
- **Instance Type**: GPU Instance
- **GPU**: NVIDIA A4000 ⚠️ **必选A4000**
- **vCPU**: 4
- **Memory**: 16Gi
- **Port**: 7860 (Public)

#### 第7步：部署
点击 **"Deploy"** 按钮

---

### 方法2：使用Python自动部署脚本

```bash
# 设置API令牌
export KOYEB_API_TOKEN="rocrorea70dhiis0zw0u68j35xve4ljjpt6ytw2sz7ixbr8y70ox7dpgqj497h28"

# 运行部署脚本
python3 deploy-koyeb.py
```

**优势**: 自动配置所有参数，无需手动操作

---

### 方法3：使用Shell脚本部署

```bash
# 设置API令牌
export KOYEB_API_TOKEN="rocrorea70dhiis0zw0u68j35xve4ljjpt6ytw2sz7ixbr8y70ox7dpgqj497h28"

# 运行部署脚本
bash deploy-koyeb.sh
```

---

## ⏱️ 部署时间表

| 阶段 | 时间 |
|------|------|
| 部署开始 | 1-2分钟 |
| 依赖安装 | 5-15分钟 |
| 模型下载 | 5-15分钟 |
| 应用启动 | 1-5分钟 |
| **总计** | **15-45分钟** |

---

## 📊 部署进度监控

### 实时查看日志
1. 打开 https://app.koyeb.com
2. 找到 "indextts-webui" 服务
3. 点击 "Logs" 标签
4. 实时查看构建日志

### 关键日志指标
- `Building...` → 正在构建
- `Running pip install` → 安装依赖
- `Downloading models...` → 下载模型（正常，可能需要10-15分钟）
- `Application started` → 应用启动成功
- `Active` → 部署完成！

---

## 🎯 部署完成后

### 1️⃣ 获取应用URL
部署完成后，Koyeb会在服务页面显示URL：
```
https://indextts-webui-xxxxx.koyeb.app
```

### 2️⃣ 访问应用
在浏览器中打开URL，等待Gradio界面加载

### 3️⃣ 开始使用
- 上传提示音频
- 输入文本（中文或英文）
- 选择情感控制模式
- 点击生成
- 享受您的AI语音！

---

## 🆘 常见问题

### Q1：部分选项找不到？
**A**: 刷新页面或清空浏览器缓存

### Q2：分支选不到正确的？
**A**: 
- 确保已连接GitHub账户
- 检查仓库是否授权给Koyeb
- 分支名：`koyeb-deploy-gpu-a4000-github-define-python`

### Q3：找不到A4000 GPU？
**A**:
- 先选择 "GPU Instance"
- 再选择 "NVIDIA A4000"
- 如果仍无法选择，检查账户配额

### Q4：部署卡住了？
**A**:
- 查看日志了解具体进度
- 通常在安装依赖或下载模型时需要等待
- 不要立即重启，耐心等待30+分钟

### Q5：应用无响应？
**A**:
- 确保服务状态是 "Active"
- 等待首次启动完成（需要初始化模型）
- 查看日志是否有错误

### Q6：模型下载失败？
**A**:
- 这通常是网络问题
- 检查Hugging Face可访问性
- 重新部署重试

---

## 📋 部署检查清单

**在点击Deploy前检查：**

- [ ] 分支: `koyeb-deploy-gpu-a4000-github-define-python`
- [ ] Python: 3.10 (runtime.txt定义)
- [ ] GPU: NVIDIA A4000
- [ ] vCPU: 4
- [ ] 内存: 16Gi
- [ ] 端口: 7860 (Public)
- [ ] 环境变量: 3个
- [ ] 运行命令: 包含 $PORT 变量

✅ **全部确认后，点击Deploy！**

---

## 💻 配置验证

所有配置已通过验证：

```
✅ Python版本定义: runtime.txt
✅ 项目依赖: requirements.txt (31个包)
✅ Koyeb构建配置: koyeb.yml
✅ GPU部署配置: .koyeb-deploy.yaml
✅ 应用入口点: webui.py
✅ Git忽略配置: .gitignore
✅ 所有关键依赖已包含
✅ 分支配置正确
✅ GPU A4000已配置
```

---

## 🔑 关键信息

| 项目 | 值 |
|------|-----|
| API令牌 | rocrorea70dhiis0zw0u68j35xve4ljjpt6ytw2sz7ixbr8y70ox7dpgqj497h28 |
| GitHub仓库 | https://github.com/nianxi666/indextts |
| 部署分支 | koyeb-deploy-gpu-a4000-github-define-python |
| Python版本 | 3.10 |
| GPU | NVIDIA A4000 |
| 服务名称 | indextts-webui |
| 端口 | 7860 |

---

## 📞 需要帮助？

- **Koyeb文档**: https://koyeb.com/docs
- **GitHub项目**: https://github.com/nianxi666/indextts
- **部署详细指南**: 查看 DEPLOY_NOW.md

---

## 🎉 准备好了吗？

所有配置都正确，代码已推送，现在就可以部署了！

### 立即开始：
1. 选择上述三种部署方式之一
2. 按照步骤操作
3. 等待20-45分钟
4. 享受您的AI语音应用！

---

**分支**: koyeb-deploy-gpu-a4000-github-define-python ✅  
**配置**: 全部正确 ✅  
**状态**: 准备部署 ✅  

**现在就开始部署吧！** 🚀
