import cv2
import numpy as np
from imutils.video import VideoStream
from yolodetect import YoloDetect

video = VideoStream('../dataset/video.mp4').start()

# chứa các điểm người dùng chọn để tạo đa giác
currentPoints = []
polygons = []

# new model Yolo
model = YoloDetect()

# nếu bấm chuột trái, điểm points sẽ tự nối lại bằng hàm append


def handle_left_click(event, x, y, flags, points):
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append([x, y])


def draw_polygon(frame, points):
    for point in points:
        frame = cv2.circle(frame, (point[0], point[1]), 5, (0, 0, 255), -1)

    frame = cv2.polylines(frame, [np.int32(points)],
                          False, (255, 0, 0), thickness=2)
    return frame


detect = False

while True:

    frame = video.read()
    frame = cv2.flip(frame, 1)

    # Ve polygon
    # frame = draw_polygon(frame, points)

    draw_polygon(frame, currentPoints)

    for points in polygons:
        frame = draw_polygon(frame, points)

    if detect:
        frame = model.detect(frame=frame, points=points)

    if detect:
        frame = model.detect(frame=frame, points=points)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    elif key == ord('d'):
        # points.append(points[0])
        currentPoints.append(currentPoints[0])
        polygons.append(currentPoints)
        currentPoints = []
        detect = True

        print(polygons)

    # Hien anh ra man hinh
    cv2.imshow("Instrusion Warning", frame)

    # cv2.setMouseCallback('Instrusion Warning', handle_left_click, points)
    cv2.setMouseCallback('Instrusion Warning',
                         handle_left_click, currentPoints)

video.stop()
cv2.destroyAllWindows()
