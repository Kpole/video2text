import pathlib

import whisper
import os
from tqdm import tqdm
from pathlib import Path
import torch

whisper_model = None

def load_whisper(model="tiny"):
    global whisper_model
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    whisper_model = whisper.load_model(model, device=device)
    print(f"Whisper模型: [{model}], device: [{device}]")


def run_analysis(audio_path, file_name, out_path, model="tiny", prompt="以下是普通话的句子。"):
    global whisper_model
    if whisper_model is None:
        load_whisper(model)
    print("正在加载Whisper模型...")
    # 读取列表中的音频文件
    audio_list = os.listdir(audio_path)
    audio_path = Path(audio_path)
    out_path = Path(out_path)
    print("加载Whisper模型成功！")
    # 创建outputs文件夹
    os.makedirs(out_path, exist_ok=True)
    print("正在转换文本...")

    i = 1
    for fn in audio_list:
        print(f"正在转换第{i}/{len(audio_list)}个音频...")
        # 识别音频
        result = whisper_model.transcribe((audio_path / fn).__str__(), initial_prompt=prompt)
        print("".join([item["text"] for item in result["segments"] if item is not None]))

        with open(out_path / f"{file_name}.txt", "a", encoding="utf-8") as f:
            f.write("".join([item["text"] for item in result["segments"] if item is not None]))
            f.write("\n")
        i += 1

