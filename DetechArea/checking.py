from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import cv2
import json
from object_detection import ObjectDetection
od = ObjectDetection()

# array of res = {start_time, end_time, count}
data = []


def is_inside(points, centroid):
    # check a point that in polygon
    polygon = Polygon(points)
    centroid = Point(centroid)
    return polygon.contains(centroid)


def compare_polygons(polygons, centroid, clock, list_results_by_frame):
    # compare a point inside which polygons?
    # print('aaaaaaa')
    print(list_results_by_frame)
    for idx, polygon in enumerate(polygons):
        if (is_inside(polygon, centroid)):
            print(list_results_by_frame[idx])
            list_results_by_frame[idx]['count'] += 1
            list_results_by_frame[idx]['start_time'] = str(clock)
            break


def recheck_area(clock, list_results_by_frame):
    # check the polygon that contain person in each frame?
    for idx, area in enumerate(list_results_by_frame):
        if (area['count'] == 0):
            list_results_by_frame[idx]['end_time'] = str(clock)


def checking(frame, polygons, clock):
    (class_ids, scores, boxes) = od.detect(frame)
    list_results_by_frame = []
    for idx in enumerate(polygons):
        res = {
            'start_time': '0',
            'end_time': '0',
            'count': 0
        }
        list_results_by_frame.append(res)

    for box in boxes:
        (x, y, w, h) = box
        cx = int((x + x + w) / 2)
        cy = int((y + y + h) / 2)
        compare_polygons(polygons=polygons, centroid=(cx, cy),
                         clock=clock, list_results_by_frame=list_results_by_frame)
        recheck_area(clock=clock, list_results_by_frame=list_results_by_frame)
        data.append(list_results_by_frame)
        data_to_json()
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)


def data_to_json():
    json_object = json.dumps(data)
    file_name = 'results.json'
    with open(file_name, "w") as outfile:
        outfile.write(json_object)
