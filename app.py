#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
LongCat-AudioDiT Gradio WebUI
简单易用的 TTS 和语音克隆界面
"""

import gradio as gr
import torch
import soundfile as sf
import os
from audiodit import AudioDiTModel
from transformers import AutoTokenizer
import librosa

# 全局变量
model = None
tokenizer = None
model_path = None

def load_model(model_size):
    """加载模型"""
    global model, tokenizer, model_path
    
    if model_size == "1B":
        model_path = "models/LongCat-AudioDiT-1B"
    else:
        model_path = "models/LongCat-AudioDiT-3.5B"
    
    if not os.path.exists(model_path):
        return f"❌ 模型不存在：{model_path}\n请先下载模型！"
    
    try:
        print(f"Loading model: {model_path}...")
        model = AudioDiTModel.from_pretrained(
            model_path,
            torch_dtype=torch.float16
        ).to("cuda")
        
        model.vae.to_half()
        model.eval()
        
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        
        return f"✅ 模型加载成功：{model_size}"
    except Exception as e:
        return f"❌ 模型加载失败：{str(e)}"

def generate_speech(text, duration, steps, cfg_strength, guidance_method, model_size):
    """生成语音"""
    global model, tokenizer
    
    if model is None:
        load_model(model_size)
    
    if model is None:
        return None, "❌ 模型未加载"
    
    try:
        # 文本编码
        inputs = tokenizer([text], padding="longest", return_tensors="pt").to("cuda")
        
        # 生成音频
        with torch.no_grad():
            output = model(
                input_ids=inputs.input_ids,
                attention_mask=inputs.attention_mask,
                duration=int(duration),
                steps=int(steps),
                cfg_strength=float(cfg_strength),
                guidance_method=guidance_method,
            )
        
        # 保存临时文件
        output_path = "output_temp.wav"
        sf.write(output_path, output.waveform.squeeze().cpu().numpy(), 24000)
        
        return output_path, f"✅ 生成成功！时长：{duration} 帧"
    
    except Exception as e:
        return None, f"❌ 生成失败：{str(e)}"

def voice_clone(text, prompt_text, prompt_audio, duration, steps, cfg_strength, model_size):
    """语音克隆"""
    global model, tokenizer
    
    if model is None:
        load_model(model_size)
    
    if model is None:
        return None, "❌ 模型未加载"
    
    if prompt_audio is None:
        return None, "❌ 请上传参考音频"
    
    try:
        # 加载音频
        audio, sr = librosa.load(prompt_audio, sr=24000)
        audio_tensor = torch.from_numpy(audio).unsqueeze(0).to("cuda")
        
        # 文本编码
        inputs = tokenizer([text], padding="longest", return_tensors="pt").to("cuda")
        prompt_inputs = tokenizer([prompt_text], padding="longest", return_tensors="pt").to("cuda")
        
        # 生成音频
        with torch.no_grad():
            output = model(
                input_ids=inputs.input_ids,
                attention_mask=inputs.attention_mask,
                prompt_audio=audio_tensor,
                prompt_input_ids=prompt_inputs.input_ids,
                prompt_attention_mask=prompt_inputs.attention_mask,
                duration=int(duration),
                steps=int(steps),
                cfg_strength=float(cfg_strength),
                guidance_method="apg",  # 语音克隆必须用 apg
            )
        
        # 保存临时文件
        output_path = "cloned_temp.wav"
        sf.write(output_path, output.waveform.squeeze().cpu().numpy(), 24000)
        
        return output_path, f"✅ 语音克隆成功！时长：{duration} 帧"
    
    except Exception as e:
        return None, f"❌ 克隆失败：{str(e)}"

def create_ui():
    """创建界面"""
    with gr.Blocks(title="LongCat-AudioDiT WebUI", theme=gr.themes.Soft()) as demo:
        gr.Markdown("""
        # 🎙️ LongCat-AudioDiT WebUI
        美团开源的 SOTA TTS 模型 - 支持文本转语音和语音克隆
        
        **特点：**
        - 🚀 中文语音克隆 SOTA（SIM 0.818）
        - 🎯 支持 1B 和 3.5B 两种模型
        - 🎨 简单易用的 Web 界面
        """)
        
        with gr.Tabs():
            # Tab 1: TTS
            with gr.TabItem("📝 TTS 文本转语音"):
                gr.Markdown("### 将文本转换为语音")
                
                with gr.Row():
                    with gr.Column():
                        text_input = gr.Textbox(
                            label="输入文本",
                            placeholder="请输入要转换的文本...",
                            lines=3,
                            value="今天晴暖转阴雨，空气质量优至良，空气相对湿度较低。"
                        )
                        
                        with gr.Row():
                            duration_slider = gr.Slider(
                                minimum=10,
                                maximum=200,
                                value=62,
                                step=1,
                                label="时长（帧数）"
                            )
                            steps_slider = gr.Slider(
                                minimum=8,
                                maximum=50,
                                value=16,
                                step=1,
                                label="采样步数"
                            )
                        
                        with gr.Row():
                            cfg_slider = gr.Slider(
                                minimum=1.0,
                                maximum=10.0,
                                value=4.0,
                                step=0.5,
                                label="CFG 强度"
                            )
                            guidance_method = gr.Radio(
                                choices=["cfg", "apg"],
                                value="cfg",
                                label="引导方法"
                            )
                        
                        model_size_tts = gr.Radio(
                            choices=["1B", "3.5B"],
                            value="1B",
                            label="模型大小"
                        )
                        
                        tts_button = gr.Button("🎤 生成语音", variant="primary")
                    
                    with gr.Column():
                        tts_output = gr.Audio(label="生成的音频")
                        tts_status = gr.Textbox(label="状态")
                
                tts_button.click(
                    fn=generate_speech,
                    inputs=[
                        text_input,
                        duration_slider,
                        steps_slider,
                        cfg_slider,
                        guidance_method,
                        model_size_tts
                    ],
                    outputs=[tts_output, tts_status]
                )
            
            # Tab 2: 语音克隆
            with gr.TabItem("🎭 语音克隆"):
                gr.Markdown("### 使用参考音频克隆语音")
                
                with gr.Row():
                    with gr.Column():
                        clone_text = gr.Textbox(
                            label="目标文本",
                            placeholder="请输入要用参考声音说的文本...",
                            lines=3,
                            value="今天晴暖转阴雨，空气质量优至良。"
                        )
                        
                        prompt_text = gr.Textbox(
                            label="参考音频文本",
                            placeholder="参考音频说的内容...",
                            lines=2,
                            value="小偷却一点也不气馁，继续在抽屉里翻找。"
                        )
                        
                        prompt_audio = gr.Audio(
                            label="参考音频",
                            type="filepath"
                        )
                        
                        with gr.Row():
                            clone_duration = gr.Slider(
                                minimum=10,
                                maximum=200,
                                value=62,
                                step=1,
                                label="时长（帧数）"
                            )
                            clone_steps = gr.Slider(
                                minimum=8,
                                maximum=50,
                                value=16,
                                step=1,
                                label="采样步数"
                            )
                        
                        clone_cfg = gr.Slider(
                            minimum=1.0,
                            maximum=10.0,
                            value=4.0,
                            step=0.5,
                            label="CFG 强度"
                        )
                        
                        model_size_clone = gr.Radio(
                            choices=["1B", "3.5B"],
                            value="1B",
                            label="模型大小"
                        )
                        
                        clone_button = gr.Button("🎭 克隆语音", variant="primary")
                    
                    with gr.Column():
                        clone_output = gr.Audio(label="克隆的音频")
                        clone_status = gr.Textbox(label="状态")
                
                clone_button.click(
                    fn=voice_clone,
                    inputs=[
                        clone_text,
                        prompt_text,
                        prompt_audio,
                        clone_duration,
                        clone_steps,
                        clone_cfg,
                        model_size_clone
                    ],
                    outputs=[clone_output, clone_status]
                )
            
            # Tab 3: 模型管理
            with gr.TabItem("⚙️ 模型管理"):
                gr.Markdown("### 加载和管理模型")
                
                with gr.Row():
                    load_model_size = gr.Radio(
                        choices=["1B", "3.5B"],
                        value="1B",
                        label="选择模型"
                    )
                    load_button = gr.Button("📥 加载模型", variant="primary")
                
                model_status = gr.Textbox(label="模型状态", lines=3)
                
                load_button.click(
                    fn=load_model,
                    inputs=[load_model_size],
                    outputs=[model_status]
                )
                
                gr.Markdown("""
                ### 📥 模型下载
                
                如果模型未下载，请先下载：
                
                **方法 1: 使用 HuggingFace CLI**
                ```bash
                huggingface-cli download meituan-longcat/LongCat-AudioDiT-1B --local-dir models/LongCat-AudioDiT-1B
                ```
                
                **方法 2: 手动下载**
                访问 https://huggingface.co/meituan-longcat/LongCat-AudioDiT-1B 下载所有文件到 `models/LongCat-AudioDiT-1B/` 目录
                """)
        
        gr.Markdown("""
        ---
        **💡 使用提示：**
        - 时长（帧数）：决定生成音频的长度，一般 60-80 帧对应 10 秒左右
        - 采样步数：越多质量越好，但速度越慢（推荐 16-24）
        - CFG 强度：越高越遵循文本，但可能不自然（推荐 3.0-5.0）
        - 语音克隆必须使用 **apg** 引导方法
        
        **⚠️ 注意事项：**
        - 需要 NVIDIA 显卡（推荐 RTX 3060 及以上）
        - 1B 版本需要约 6GB 显存，3.5B 版本需要约 14GB 显存
        - 首次运行会加载模型，需要一些时间
        """)
    
    return demo

if __name__ == "__main__":
    # 创建模型目录
    os.makedirs("models", exist_ok=True)
    
    # 创建界面
    demo = create_ui()
    
    # 启动服务
    print("🚀 启动 LongCat-AudioDiT WebUI...")
    print("📱 访问地址：http://localhost:7860")
    demo.launch(server_name="0.0.0.0", server_port=7860)
