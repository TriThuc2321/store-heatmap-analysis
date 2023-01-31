import cv2
import numpy as np
from imutils.video import VideoStream
import json
from checking import checking
import datetime
from analyst import analyst_to_excel
import os


# chứa các điểm người dùng chọn để tạo đa giác
# points1 = [[100, 200], [100, 300], [200, 150], [100, 200]]
# points2 = [[300, 400], [300, 500], [400, 250], [300, 400]]
# polygon = [points1, points2]

currentPoints = []
polygons = []
file_name = 'data/area.json'

title = "Press: a (add point), z(delete all area), d (delete point), ENTER (start ananlyst)"

FRAME_PER_SECOND = 100


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
    dialog.Show()
    print(datetime.datetime.now())
    cv2.destroyWindow(title)
    cv2.destroyAllWindows()
    video = VideoStream(VIDEO_DATASET).start()
    count = 0
    while True:
        frame = video.read()
        key = cv2.waitKey(int(1000/FRAME_PER_SECOND))
        if key == ord('q'):
            break
        for idx, list_points in enumerate(polygons):
            frame = draw_polygon(frame, list_points, idx)
        try:
            checking(frame=frame, polygons=polygons, is_end=False)
            count += 1
        except Exception as e:
            checking(frame=frame, polygons=polygons, is_end=True)
            print(str(e))
            print("Actual frame: " + str(count))
            break

        # cv2.imshow("Calculate", frame)

    video.stop()
    print(datetime.datetime.now())
    analyst_to_excel(count, number_of_frames_origin, fps_origin)

    cv2.destroyAllWindows()
    dialog.SetTitle("Done!!")
    dialog.set_message("Progress done!")
    dialog.Show()


detect = []


def polygons_to_json():
    json_object = json.dumps(polygons)

    try:
        folder_data_existed = os.path.exists("data")
        if (folder_data_existed == False):
            os.makedirs("data")
        with open(file_name, "w") as outfile:
            outfile.write(json_object)
    except Exception as e:
        print(e)


def json_to_polygons():
    try:
        with open(file_name, 'r') as openfile:
            return json.load(openfile)
    except IOError:
        return []


def runApplication(progress_dialog, video_path):
    global currentPoints
    global polygons
    global number_of_frames_origin
    global fps_origin
    global dialog
    global VIDEO_DATASET
    dialog = progress_dialog

    polygons = json_to_polygons()
    VIDEO_DATASET = str(video_path)
    video = VideoStream(VIDEO_DATASET).start()
    cap = cv2.VideoCapture(VIDEO_DATASET)
    number_of_frames_origin = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps_origin = int(cap.get(cv2.CAP_PROP_FPS))
    print(number_of_frames_origin, fps_origin)

    while True:

        frame = video.read()

        draw_polygon(frame, currentPoints, len(polygons))
        # Ve polygon
        for idx, points in enumerate(polygons):
            frame = draw_polygon(frame, points, idx)

        key = cv2.waitKey(1)

        if key == ord('q'):
            break
        elif key == ord('a'):
            if currentPoints:
                currentPoints.append(currentPoints[0])
                polygons.append(currentPoints)
            currentPoints = []
        elif key == ord('z'):
            polygons = []
            currentPoints = []

        elif key == ord('d'):
            if currentPoints:
                currentPoints.pop()
            elif polygons:
                polygons.pop()
        elif key == ord('\r'):
            polygons_to_json()
            video.stop()
            progress_cal()
            break

        cv2.imshow(title, frame)

        cv2.setMouseCallback(title,
                             handle_left_click, currentPoints)
