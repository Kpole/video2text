import math

from moviepy.editor import VideoFileClip
from pydub import AudioSegment
from pathlib import Path
from tqdm import tqdm
import os

import time

def extract_audio(video_path, video_name, out_path, verbose=False):
    """
    将 video 转换为 audio，即视频转为音频
    :param video_path: video 路径
    :param video_name: 文件名
    :param out_path: 目标路径
    :param verbose: 是否显示详情
    :return: None
    """
    clip = VideoFileClip(video_path)
    audio = clip.audio
    out_path = Path(out_path) / f"{video_name}.mp3"
    audio.write_audiofile(out_path, logger='bar' if verbose else None)
    return out_path

def split_mp3(audio_path, video_name, out_path, slice_length=60000, verbose=False):
    """
    切割 audio 文件，默认每份不超过 1 分钟
    :param audio_path: audio 文件目录
    :param video_name: 文件名
    :param out_path: 目标路径
    :param slice_length: 切割长度，默认为 60s
    :param verbose: 是否显示详情
    :return:
    """
    audio = AudioSegment.from_mp3(audio_path)
    slices_count = math.ceil(len(audio) / slice_length)

    out_path = Path(out_path) / video_name
    os.makedirs(out_path, exist_ok=True)
    bar = tqdm(total=slices_count, desc="视频切割")
    for i in range(slices_count):
        begin = i * slice_length
        end = begin + slice_length
        audio_slice = audio[begin:end]
        file_path = out_path / f"{i+1}.mp3"
        audio_slice.export(file_path)
        bar.update(1)

    print("视频切割完成")

    return out_path

# 使用示例
def split(video_name, input_path, verbose=False):
    # video_name = r"摆拍，编剧本，网红上热搜，短视频是怎样恶心全国的？【围炉夜话】"
    out_path = r"D:\hyd\code\video2text\audio"
    # input_path = r"D:\hyd\code\video2text\video\摆拍，编剧本，网红上热搜，短视频是怎样恶心全国的？【围炉夜话】.flv"
    audio_path = extract_audio(input_path,
                  video_name=video_name,
                  out_path=out_path,
                  verbose=verbose)
    out_path = split_mp3(audio_path, video_name, out_path, verbose=verbose)
    return out_path