# 🎙️ LongCat-AudioDiT WebUI

美团开源的 SOTA TTS 模型 - 简单易用的 Web 界面

## ✨ 特性

- 🚀 **中文语音克隆 SOTA** - SIM 分数 0.818，超越 Seed-DiT
- 🎯 **两种模型** - 1B（6GB 显存）和 3.5B（14GB 显存）
- 🎨 **Web 界面** - 无需命令行，浏览器即可使用
- 🎭 **语音克隆** - 上传参考音频即可克隆声音
- 📱 **远程访问** - 支持局域网访问

---

## 🚀 快速开始

### Windows 用户（推荐）

1. **下载项目**
   ```cmd
   mkdir C:\AI\TTS
   cd C:\AI\TTS
   git clone https://github.com/Bowerai/longcat-tts-webui.git
   cd longcat-tts-webui
   ```

2. **下载模型**
   ```cmd
   pip install huggingface_hub
   huggingface-cli download meituan-longcat/LongCat-AudioDiT-1B --local-dir models/LongCat-AudioDiT-1B
   ```

3. **一键启动**
   ```cmd
   start.bat
   ```

4. **访问界面**
   - 浏览器打开：http://localhost:7860

---

## 📦 安装说明

### 前置要求

- **系统**: Windows 10/11 (64 位)
- **Python**: 3.10 或更高版本
- **显卡**: NVIDIA RTX 3060 及以上（推荐）
- **显存**: 
  - 1B 版本：至少 6GB
  - 3.5B 版本：至少 14GB

### 手动安装

```cmd
# 1. 创建虚拟环境
python -m venv venv
venv\Scripts\activate

# 2. 安装依赖
pip install -r requirements.txt

# 3. 安装 PyTorch CUDA 版本
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# 4. 下载模型
huggingface-cli download meituan-longcat/LongCat-AudioDiT-1B --local-dir models/LongCat-AudioDiT-1B

# 5. 启动
python app.py
```

---

## 🎯 使用指南

### TTS 文本转语音

1. 在 **TTS 文本转语音** 标签页
2. 输入要转换的文本
3. 调整参数（可选）：
   - **时长**：60-80 帧对应约 10 秒
   - **采样步数**：16-24（推荐）
   - **CFG 强度**：3.0-5.0（推荐）
4. 点击 **生成语音**
5. 试听并下载音频

### 语音克隆

1. 在 **语音克隆** 标签页
2. 上传参考音频（WAV 格式，1-10 秒）
3. 输入参考音频的文本内容
4. 输入要用该声音说的目标文本
5. 调整参数（可选）
6. 点击 **克隆语音**
7. 试听并下载音频

---

## ⚙️ 参数说明

| 参数 | 说明 | 推荐值 |
|------|------|--------|
| **时长（帧数）** | 决定音频长度 | 60-80 帧（10 秒） |
| **采样步数** | 扩散步数，越多质量越好 | 16-24 |
| **CFG 强度** | 遵循文本的程度 | 3.0-5.0 |
| **引导方法** | TTS 用 cfg，克隆用 apg | cfg / apg |

---

## ❓ 常见问题

### Q: 提示 CUDA out of memory
**A:** 减小"时长"参数，或使用 1B 版本而不是 3.5B 版本。

### Q: 模型加载失败
**A:** 确认模型已正确下载到 `models/LongCat-AudioDiT-1B/` 目录。

### Q: 生成速度很慢
**A:** 减少"采样步数"到 12-16，可以显著提升速度。

### Q: 语音克隆效果不好
**A:** 
- 确保参考音频清晰（1-10 秒）
- 确保参考音频文本准确
- 使用 **apg** 引导方法

---

## 📊 性能预期

| 显卡 | 1B 版本 | 3.5B 版本 |
|------|--------|----------|
| RTX 3060 (12GB) | ✅ 可用 | ❌ 显存不足 |
| RTX 3080 (10GB) | ✅ 可用 | ⚠️ 可能 OOM |
| RTX 3090 (24GB) | ✅ 快速 | ✅ 可用 |
| RTX 4070 (12GB) | ✅ 可用 | ⚠️ 可能 OOM |
| RTX 4090 (24GB) | ✅ 快速 | ✅ 快速 |

**生成速度（10 秒音频）：**
- 1B 版本：~30-60 秒
- 3.5B 版本：~60-120 秒

---

## 📁 目录结构

```
longcat-tts-webui/
├── app.py                 # 主程序
├── requirements.txt       # 依赖列表
├── start.bat             # Windows 启动脚本
├── README.md             # 说明文档
└── models/               # 模型目录
    ├── LongCat-AudioDiT-1B/
    └── LongCat-AudioDiT-3.5B/
```

---

## 🔗 相关链接

- **原项目**: https://github.com/meituan-longcat/LongCat-AudioDiT
- **1B 模型**: https://huggingface.co/meituan-longcat/LongCat-AudioDiT-1B
- **3.5B 模型**: https://huggingface.co/meituan-longcat/LongCat-AudioDiT-3.5B
- **技术报告**: https://arxiv.org/abs/2603.29339

---

## 📄 许可证

MIT License

---

## 💡 致谢

- **美团 LongCat 团队** - 开源优秀的 TTS 模型
- **Gradio 团队** - 提供易用的 WebUI 框架

---

**祝你使用愉快！** 🎉
