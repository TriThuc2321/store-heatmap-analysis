import cv2
import numpy as np
from object_detection_origin import ObjectDetection
import math
import datetime

# Initialize Object Detection
od = ObjectDetection()

cap = cv2.VideoCapture("los_angeles.mp4")

# Initialize count
count = 0
center_points_prev_frame = []

tracking_objects = {}
track_id = 0

object_id_list = []
dtime = dict()
dwell_time = dict()

while True:
    ret, frame = cap.read()
    count += 1
    if not ret:
        break

    # Point current frame
    center_points_cur_frame = []

    # Detect objects on frame
    (class_ids, scores, boxes) = od.detect(frame)
    for box in boxes:
        (x, y, w, h) = box
        cx = int((x + x + w) / 2)
        cy = int((y + y + h) / 2)
        center_points_cur_frame.append((cx, cy))
        #print("FRAME N°", count, " ", x, y, w, h)

        # cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Only at the beginning we compare previous and current frame
    if count <= 2:
        for pt in center_points_cur_frame:
            for pt2 in center_points_prev_frame:
                distance = math.hypot(pt2[0] - pt[0], pt2[1] - pt[1])

                if distance < 20:
                    tracking_objects[track_id] = pt
                    track_id += 1
                    object_id_list.append(track_id)
                    dtime[track_id] = datetime.datetime.now()
                    dwell_time[track_id] = 0
    else:

        tracking_objects_copy = tracking_objects.copy()
        center_points_cur_frame_copy = center_points_cur_frame.copy()

        for object_id, pt2 in tracking_objects_copy.items():
            object_exists = False
            for pt in center_points_cur_frame_copy:
                distance = math.hypot(pt2[0] - pt[0], pt2[1] - pt[1])

                # Update IDs position
                if distance < 20:
                    tracking_objects[object_id] = pt
                    object_exists = True

                    if object_id not in object_id_list:
                        object_id_list.append(object_id)
                        dtime[object_id] = datetime.datetime.now()
                        dwell_time[object_id] = 0
                    else:
                        curr_time = datetime.datetime.now()
                        old_time = dtime[object_id]
                        time_diff = curr_time - old_time
                        dtime[object_id] = datetime.datetime.now()
                        sec = time_diff.seconds
                        dwell_time[object_id] += sec

                    if pt in center_points_cur_frame:
                        center_points_cur_frame.remove(pt)
                    continue

            # Remove IDs lost
            if not object_exists:
                tracking_objects.pop(object_id)

        # Add new IDs found
        for pt in center_points_cur_frame:
            tracking_objects[track_id] = pt
            track_id += 1
            if object_id not in object_id_list:
                object_id_list.append(object_id)
                dtime[object_id] = datetime.datetime.now()
                dwell_time[object_id] = 0
            else:
                curr_time = datetime.datetime.now()
                old_time = dtime[object_id]
                time_diff = curr_time - old_time
                dtime[object_id] = datetime.datetime.now()
                sec = time_diff.seconds
                dwell_time[object_id] += sec

    for object_id, pt in tracking_objects.items():
        print("\n" + str(object_id))
        print("dwell_time", dwell_time)
        label = str(object_id)
        if (object_id not in dwell_time):
            continue
        label += "-" + str(dwell_time[object_id])
        # + str(dwell_time[object_id + 1])
        cv2.circle(frame, pt, 5, (0, 0, 255), -1)
        cv2.putText(frame, label,
                    (pt[0], pt[1] - 7), 0, 0.8, (0, 0, 255), 2)

    # print("Tracking objects")
    # print(tracking_objects)

    # print("CUR FRAME LEFT PTS")
    # print(center_points_cur_frame)

    cv2.imshow("Frame", frame)

    # Make a copy of the points
    center_points_prev_frame = center_points_cur_frame.copy()

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
