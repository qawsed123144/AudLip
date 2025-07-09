import cv2
from mouth_tracker import MouthTracker
from audio_recorder import record
from asr_engine import transcribe
from concurrent.futures import ProcessPoolExecutor

executor = ProcessPoolExecutor(max_workers=1)

# 設定
RECORD_SECONDS = 5
FS = 16000
CHANNELS = 1

def process_segment(idx):
    filename = f"segment_{idx:03d}.wav"
    record(RECORD_SECONDS, FS, CHANNELS, filename)
    text = transcribe(filename)
    print(f"Caption: {text}")

def main():
    tracker = MouthTracker(threshold=5.0, camera_index=0)
    seg_idx = 0
    prev_talking = False

    for frame, talking in tracker.stream():
        if talking and not prev_talking:
            executor.submit(process_segment, seg_idx)
            seg_idx += 1
        prev_talking = talking
        cv2.imshow("Live Caption", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()