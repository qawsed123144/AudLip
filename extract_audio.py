import sys
import os
import subprocess

def extract_audio_ffmpeg(video_path, output_path=None):
    if not os.path.isfile(video_path):
        print(f"❌ 找不到檔案: {video_path}")
        return

    if output_path is None:
        base, _ = os.path.splitext(video_path)
        output_path = f"{base}.wav"

    cmd = [
        "ffmpeg",
        "-y",                      # 覆寫輸出檔案
        "-i", video_path,
        "-vn",                     # 不要影像
        "-acodec", "pcm_s16le",    # 儲存為無損 wav 格式
        "-ar", "44100",            # 取樣率
        "-ac", "2",                # 雙聲道
        output_path
    ]

    try:
        print(f"▶️ 正在抽取音訊: {video_path} → {output_path}")
        subprocess.run(cmd, check=True)
        print(f"✅ 音訊已儲存至: {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ ffmpeg 錯誤: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("📌 用法: python extract_audio.py <影片路徑> [輸出音訊路徑]")
    else:
        video_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else None
        extract_audio_ffmpeg(video_file, output_file)