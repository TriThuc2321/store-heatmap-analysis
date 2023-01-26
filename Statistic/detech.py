import cv2
import numpy as np
from imutils.video import VideoStream
from yolodetect import YoloDetect
import json

video = VideoStream('../dataset/video.mp4').start()

vid = cv2.VideoCapture(1)

# chứa các điểm người dùng chọn để tạo đa giác
currentPoints = []
polygons = []
file_name = 'polygons.json'

# new model Yolo
model = YoloDetect()

# nếu bấm chuột trái, điểm points sẽ tự nối lại bằng hàm append


def handle_left_click(event, x, y, flags, points):
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append([x, y])

# draw polygon


def draw_polygon(frame, points):
    for point in points:
        frame = cv2.circle(frame, (point[0], point[1]), 5, (0, 0, 255), -1)

    frame = cv2.polylines(frame, [np.int32(points)],
                          False, (255, 0, 0), thickness=2)
    return frame


# set Yolo được phép detect chưa
detect = True


def polygons_to_json():
    json_object = json.dumps(polygons)

    with open(file_name, "w") as outfile:
        outfile.write(json_object)

# draw polygons from json


def json_to_polygons():
    try:
        with open(file_name, 'r') as openfile:
            return json.load(openfile)
    except IOError:
        return []


polygons = json_to_polygons()


def runDetech():
    global currentPoints
    global polygons
    global detect
    
    while True:

        #     frame = vid.read()

        #     cv2.imshow('cameraaaaa', frame )
        #     key = cv2.waitKey(1)
        #     if key == ord('q'):
        #         break

        # video.stop()
        # cv2.destroyAllWindows()

        frame = video.read()
        frame = cv2.flip(frame, 1)

        # Ve polygon
        # frame = draw_polygon(frame, points)

        draw_polygon(frame, currentPoints)

        for points in polygons:
            frame = draw_polygon(frame, points)

            if detect:
                frame = model.detect(frame=frame, points=points)

        key = cv2.waitKey(1)
        if key == ord('q'):
            break

        # Bấm a để nối 2 điểm còn lại của polygons
        elif key == ord('a'):
            if currentPoints:
                currentPoints.append(currentPoints[0])
                polygons.append(currentPoints)
            currentPoints = []
            detect = True
            print(polygons)

        # Bấm d để xóa mỗi cạnh của polygon
        elif key == ord('d'):

            print('d')
            if currentPoints:
                currentPoints.pop()
            elif polygons:
                polygons.pop()

        # Bấm s để trích polygons thành lưu tọa độ vào json
        elif key == ord('s'):
            polygons_to_json()
            break

        # Hien anh ra man hinh
        cv2.imshow("Instrusion Warning", frame)

        # cv2.setMouseCallback('Instrusion Warning', handle_left_click, points)
        cv2.setMouseCallback('Instrusion Warning',
                             handle_left_click, currentPoints)

    video.stop()
    cv2.destroyAllWindows()
