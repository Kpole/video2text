import argparse
import pathlib
from lib.split import split as split_fun
from lib.transformer import run_analysis

'''
python video2text --input_path {video_path} \
                  --output_path {output_path} \
                  --model [tiny, small, medium, large]
                  --split
                  --verbose


'''

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_path', type=str, required=True)
    parser.add_argument('-o', '--output_path', type=str, required=True)
    parser.add_argument('-m', '--model', type=str, default='tiny', help='[tiny, small, medium, large]')
    parser.add_argument('--split', action='store_true', required=False, help='将语音切割成每分钟一段')
    parser.add_argument('--audio_path', type=str, required=False, help='语音文件目录')
    parser.add_argument('--verbose', action='store_true', required=False, help='显示详情')

    args = parser.parse_args()
    print(args)


    input_path = pathlib.Path(args.input_path)
    output_path = pathlib.Path(args.output_path)
    model = args.model
    split = args.split
    audio_path = args.audio_path
    verbose = args.verbose

    if not split and not audio_path:
        raise Exception('split 为 False 时 audio_path 不能为空')

    video_file_name = input_path.name.strip(input_path.suffix)

    # video_file_name = f"{video_file_name}_{model}"
    print(video_file_name)

    if split:
        audio_path = split_fun(video_file_name, input_path.__str__(), verbose)

    run_analysis(audio_path, video_file_name, output_path, model)

if __name__ == '__main__':
    main()