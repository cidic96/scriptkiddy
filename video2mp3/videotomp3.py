# ./videotomp3.py     "/Users/sid/Library/CloudStorage/GoogleDrive-s@tryvinci.com/My Drive/Vinci Master/Creators/PreviewTemplates/PreviewVideos"        "/Users/sid/Library/CloudStorage/GoogleDrive-s@tryvinci.com/My Drive/Vinci Master/Creators/PreviewTemplates/PreviewAudios"

#!/usr/bin/env python3

import os
import subprocess
import argparse
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

def convert_to_mp3(input_file, output_file):
    command = [
        "ffmpeg",
        "-i", input_file,
        "-vn",
        "-acodec", "libmp3lame",
        "-q:a", "2",
        output_file
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def process_file(file, input_dir, output_dir):
    input_path = os.path.join(input_dir, file)
    output_path = os.path.join(output_dir, os.path.splitext(file)[0] + ".mp3")
    convert_to_mp3(input_path, output_path)
    return file

def main():
    parser = argparse.ArgumentParser(description="Convert video files to MP3 audio.")
    parser.add_argument("input_dir", help="Input directory containing video files")
    parser.add_argument("output_dir", help="Output directory for MP3 files")
    args = parser.parse_args()

    input_dir = os.path.abspath(args.input_dir)
    output_dir = os.path.abspath(args.output_dir)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv']
    video_files = [f for f in os.listdir(input_dir) if os.path.splitext(f)[1].lower() in video_extensions]

    if not video_files:
        print("No video files found in the input directory.")
        return

    print(f"Found {len(video_files)} video files. Starting conversion...")

    with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        futures = [executor.submit(process_file, file, input_dir, output_dir) for file in video_files]
        for _ in tqdm(futures, total=len(video_files), desc="Converting", unit="file"):
            _.result()

    print("Conversion complete!")

if __name__ == "__main__":
    main()