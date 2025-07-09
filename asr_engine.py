import whisper

# 載入模型，只載入一次
model = whisper.load_model("small")

def transcribe(wav_path):
    """
    使用本地 Whisper 模型做語音辨識
    :param wav_path: WAV 音檔路徑
    :return: 辨識文字
    """
    result = model.transcribe(wav_path)
    return result["text"].strip()
