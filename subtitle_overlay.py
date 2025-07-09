import cv2

def display_subtitle(frame, text, position=None, font_scale=1.0, thickness=2):
    """
    在影像上疊加字幕文字
    :param frame: OpenCV 影像
    :param text: 要顯示的文字
    :param position: (x, y) 起始座標，預設畫面底部偏左
    :param font_scale: 文字大小
    :param thickness: 文字粗細
    """
    h, w, _ = frame.shape
    if position is None:
        x = int(w * 0.05)
        y = int(h * 0.9)
    else:
        x, y = position

    # 計算文字尺寸與背景
    (text_w, text_h), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)
    cv2.rectangle(
        frame,
        (x - 5, y - text_h - 5),
        (x + text_w + 5, y + 5),
        (0, 0, 0),
        cv2.FILLED
    )
    cv2.putText(
        frame,
        text,
        (x, y),
        cv2.FONT_HERSHEY_SIMPLEX,
        font_scale,
        (255, 255, 255),
        thickness,
        cv2.LINE_AA
    )
