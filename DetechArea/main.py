import cv2
import numpy as np
from imutils.video import VideoStream
import json
# from yolodetect import YoloDetect

video = VideoStream('../dataset/video.mp4').start()
# chứa các điểm người dùng chọn để tạo đa giác
# points1 = [[100, 200], [100, 300], [200, 150], [100, 200]]
# points2 = [[300, 400], [300, 500], [400, 250], [300, 400]]
# polygon = [points1, points2]

curentPoints = []
polygons = []
file_name = 'polygons.json'


def handle_left_click(event, x, y, flags, points):
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append([x, y])


def draw_polygon(frame, points):
    for point in points:
        frame = cv2.circle(frame, (point[0], point[1]), 5, (0, 0, 255), -1)

    frame = cv2.polylines(frame, [np.int32(points)],
                          False, (255, 0, 0), thickness=2)
    return frame


def polygons_to_json():
    json_object = json.dumps(polygons)

    with open(file_name, "w") as outfile:
        outfile.write(json_object)


def json_to_polygons():
    try:
        with open(file_name, 'r') as openfile:
            return json.load(openfile)
    except IOError:
        return []


polygons = json_to_polygons()

while True:
    frame = video.read()
    frame = cv2.flip(frame, 1)

    draw_polygon(frame, curentPoints)
    # Ve polygon
    for points in polygons:
        frame = draw_polygon(frame, points)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

    elif key == ord('a'):
        if curentPoints:
            curentPoints.append(curentPoints[0])
            polygons.append(curentPoints)
        curentPoints = []
        # detect = True
        print(polygons)

    elif key == ord('d'):
        print('d')
        if curentPoints:
            curentPoints.pop()
        elif polygons:
            polygons.pop()

    elif key == ord('s'):
        polygons_to_json()
        break

    # Hien anh ra man hinh
    cv2.imshow("Instrusion Warning", frame)

    cv2.setMouseCallback('Instrusion Warning', handle_left_click, curentPoints)

video.stop()
cv2.destroyAllWindows()
