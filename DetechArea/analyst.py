import json
import openpyxl
import pandas as pd

file_name = 'results.json'

data = []

analyst_array = []


def json_to_data():
    try:
        with open(file_name, 'r') as openfile:
            return json.load(openfile)
    except IOError:
        return []


def analyst():
    # data la list cac frame
    data = json_to_data()
    count_per_frame_flag = []
    total_time = [0 for o in data[0]]
    start_per_frame_flag = []
    end_per_frame_flag = []

    start = "start_time"
    end = "end_time"
    cnt = "count"

    flag_update = {
        "start_time": False,
        "end_time": False
    }
    # frame_data la data cua tung frame
    for frame_idx, frame_data in enumerate(data):
        if frame_idx == 0:
            start_per_frame_flag = [o[start] for o in frame_data]
            count_per_frame_flag.append({
                "total_frame": 0,
                "total_person": 0
            })
        # area_data la tung khu vuc cua 1 frame
        for area_idx, area_data in enumerate(frame_data):
            if area_data[cnt] > 0 and flag_update[start] == True:
                start_per_frame_flag[area_idx] = area_data[start]
                flag_update[start] = False
                flag_update[end] = True
            # if (end_per_frame_flag[area_idx] > 0):
            #     total_time[area_idx] += end_per_frame_flag[area_idx] - area_data[start]
            # if area_data[start] > 0 and area_data[start] != start_per_frame_flag[area_idx]:
            #     flag_update[start] = False
            if area_data[end] > 0 and flag_update[end] == True:
                flag_update[start] = True
                flag_update[end] = False
                total_time[area_idx] += (area_data[end] -
                                         start_per_frame_flag[area_idx])
            if area_data[cnt] > 0:
                count_per_frame_flag[area_idx]["total_frame"] += 1
                count_per_frame_flag[area_idx]["total_person"] += area_data[cnt]
    print(count_per_frame_flag)
    time_list = total_time,
    count_list = [round(o["total_person"] / o["total_frame"])
                  for o in count_per_frame_flag]

    list = []
    n = len(data[0])
    for i in range(0, n):
        list.append({
            "no": i,
            "total_time": time_list[i],
            "total_person": count_list[i]
        })
    return list


def sort_per_time():
    tmp = analyst()
    tmp.sort(key=lambda x: x["total_time"], reverse=True)
    return tmp


def sort_per_count():
    tmp = analyst()
    tmp.sort(key=lambda x: x["total_person"], reverse=True)
    return tmp


def analyst_to_excel():
    path = 'analyst.xlsx'
    list = sort_per_count()

    print(list)
    data = []

    for i in range(0, len(list)):
        tmp_obj = list[i]
        data.append([tmp_obj["no"], tmp_obj["total_time"],
                    tmp_obj["total_person"]])

    df = pd.DataFrame(data, columns=['Kệ', 'Thời gian', 'Tổng số người'])
    df.to_excel(path)
