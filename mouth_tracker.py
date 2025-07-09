import cv2
import mediapipe as mp

# 提供 MouthTracker 類別，回傳 (frame, talking) 串流

class MouthTracker:
    def __init__(self, threshold=5.0, camera_index=0):
        """
        :param threshold: 唇縫張開判斷閥值（像素）
        :param camera_index: 攝影機設備索引，預設自動尋找
        """
        self.threshold = threshold
        self.cap = cv2.VideoCapture(camera_index)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 15)
        print(f"啟動攝影機 index: {camera_index}")
        width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        print(f"攝影機實際解析度: {width}x{height}，FPS: {fps}")
        self.mp_face_mesh = mp.solutions.face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        )
        # 建立嘴唇 landmark 索引
        self.LIPS_IDX = set()
        for conn in mp.solutions.face_mesh.FACEMESH_LIPS:
            self.LIPS_IDX.update(conn)

    def stream(self):
        if not self.cap.isOpened():
            print("❌ 攝影機未開啟，請確認 camera_index 是否正確，或攝影機是否被佔用")
            raise IOError("無法開啟攝影機")

        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            h, w, _ = frame.shape
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.mp_face_mesh.process(rgb)

            talking = False
            if results.multi_face_landmarks:
                lmks = results.multi_face_landmarks[0].landmark
                upper = lmks[13]
                lower = lmks[14]
                lip_dist = abs((upper.y - lower.y) * h)
                if lip_dist > self.threshold:
                    talking = True

                # 取得嘴唇 landmark 座標 (x,y)
                coords = [(int(lmks[i].x * w), int(lmks[i].y * h)) for i in self.LIPS_IDX]

                # 計算邊界框
                xs, ys = zip(*coords)
                x_min, x_max = min(xs), max(xs)
                y_min, y_max = min(ys), max(ys)

                # 畫紅色框框 (BGR: (0,0,255)), 粗度2
                cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 0, 255), 2)

            yield frame, talking

        self.cap.release()
