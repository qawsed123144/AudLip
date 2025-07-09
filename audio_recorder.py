import sounddevice as sd
import soundfile as sf
import argparse

# audio_recorder.py
# 即時錄音工具：錄製指定長度音訊並儲存為 WAV 檔

DEFAULT_FS = 16000  # 取樣頻率
DEFAULT_CHANNELS = 1  # 單聲道


def record(duration, fs=DEFAULT_FS, channels=DEFAULT_CHANNELS, output_path="output.wav"):
    """
    錄製音訊
    :param duration: 錄製秒數
    :param fs: 取樣頻率
    :param channels: 聲道數
    :param output_path: 輸出檔案路徑
    :return: 儲存的檔案路徑
    """
    print(f"🔴 開始錄音：長度 {duration}s, {fs}Hz, {channels}ch")
    # non-blocking 錄音
    data = sd.rec(int(duration * fs), samplerate=fs, channels=channels, dtype='int16')
    sd.wait()  # 等待錄音結束

    # 儲存為 WAV
    sf.write(output_path, data, fs)
    print(f"✅ 錄音完成並儲存至：{output_path}")
    return output_path


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='錄製音訊並輸出 WAV 檔')
    parser.add_argument('duration', type=float, help='錄製秒數，例如 3.5')
    parser.add_argument('-f', '--fs', type=int, default=DEFAULT_FS, help='取樣頻率，預設 16000')
    parser.add_argument('-c', '--channels', type=int, default=DEFAULT_CHANNELS, help='聲道數，預設 1')
    parser.add_argument('-o', '--output', default='output.wav', help='輸出檔案路徑')
    args = parser.parse_args()

    record(args.duration, fs=args.fs, channels=args.channels, output_path=args.output)
