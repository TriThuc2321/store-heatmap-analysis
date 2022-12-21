import cv2
import numpy as np
from imutils.video import VideoStream
import json
from checking import checking
import datetime
from analyst import analyst_to_excel

video = VideoStream('../dataset/video.mp4').start()
# chứa các điểm người dùng chọn để tạo đa giác
# points1 = [[100, 200], [100, 300], [200, 150], [100, 200]]
# points2 = [[300, 400], [300, 500], [400, 250], [300, 400]]
# polygon = [points1, points2]

curentPoints = []
polygons = []
file_name = 'area.json'

FRAME_PER_SECOND = 4


def handle_left_click(event, x, y, flags, points):
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append([x, y])


def draw_polygon(frame, points, idx):
    if (len(points) != 0):
        first_point = points[0]
        rect_text = str(idx)
        for point in points:
            frame = cv2.circle(frame, (point[0], point[1]), 5, (0, 0, 255), -1)

        frame = cv2.polylines(frame, [np.int32(points)],
                              False, (255, 0, 0), thickness=2)
        frame = cv2.putText(frame, rect_text, (first_point[0], first_point[1] + 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
        rect_text = ""
    return frame


def progress_cal():
    cv2.destroyWindow("Instrusion Warning")
    # cv2.destroyAllWindows()
    video = VideoStream('../dataset/video.mp4',
                        framerate=FRAME_PER_SECOND).start()
    begin_time = datetime.datetime.now()
    while True:
        frame = video.read()
        frame = cv2.flip(frame, 1)
        curr_time = datetime.datetime.now()
        sec = (curr_time - begin_time).seconds
        # print(sec)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
        for idx, list_points in enumerate(polygons):
            frame = draw_polygon(frame, list_points, idx)

        checking(frame=frame, polygons=polygons)

        cv2.imshow("Calculate", frame)

    video.stop()
    analyst_to_excel()
    cv2.destroyAllWindows()


detect = []


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


#polygons = json_to_polygons()

while True:

    frame = video.read()
    frame = cv2.flip(frame, 1)

    draw_polygon(frame, curentPoints, len(polygons))
    # Ve polygon
    for idx, points in enumerate(polygons):
        frame = draw_polygon(frame, points, idx)

    # if detect:
    #     frame = model.detect(frame=frame, points=points)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    elif key == ord('a'):
        if curentPoints:
            curentPoints.append(curentPoints[0])
            polygons.append(curentPoints)
        curentPoints = []
        # detect = True

    elif key == ord('d'):
        if curentPoints:
            curentPoints.pop()
        elif polygons:
            polygons.pop()
    elif key == ord('\r'):
        polygons_to_json()
        video.stop()
        progress_cal()

    # Hien anh ra man hinh
    cv2.imshow("Instrusion Warning", frame)

    cv2.setMouseCallback('Instrusion Warning', handle_left_click, curentPoints)

# video.stop()
# cv2.destroyAllWindows()
