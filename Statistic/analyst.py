import json
import openpyxl
import pandas as pd

file_name = 'results.json'

data = []

list_area = []

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
    list_area = get_area()
    count_per_frame_flag = []
    total_time = []

    cnt = "count"

    for area in list_area:
        count_per_frame_flag.append({
            "total_frame": 0,
            "total_person": 0
        })
        total_time.append(0)

    # frame_data la data cua tung frame
    for frame_idx, frame_data in enumerate(data):
        # area_data la tung khu vuc cua 1 frame
        for area_idx, area_data in enumerate(frame_data):
            if area_data[cnt] > 0:
                count_per_frame_flag[area_idx]["total_frame"] += 1
                count_per_frame_flag[area_idx]["total_person"] += area_data[cnt]
    count_list = handle_count_person_list(
        count_per_frame_flag=count_per_frame_flag)

    results = []
    n = len(list_area)

    print(total_time)

    for i in range(0, n):
        results.append({
            "no": i,
            "total_time": round(count_per_frame_flag[i]["total_frame"]/4, 2),
            "total_person": count_list[i]
        })
    return results


def handle_count_person_list(count_per_frame_flag):
    count_list = []
    for object in count_per_frame_flag:
        if (object["total_frame"] != 0):
            count_list.append(
                round(object["total_person"] / object["total_frame"]))
        else:
            count_list.append(0)
    return count_list


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
        data.append([tmp_obj["no"], normalize_time_data(tmp_obj["total_time"]),
                    tmp_obj["total_person"]])

    df = pd.DataFrame(data, columns=['Khu vực', 'Thời gian', 'Tổng số người'])
    df.to_excel(path)


def get_area():
    file_name = 'area.json'
    try:
        with open(file_name, 'r') as openfile:
            return json.load(openfile)
    except IOError:
        return []


def normalize_time_data(giay):
    gio = 0
    phut = 0
    if giay >= 60 and giay < 3600:
        phut = (giay-giay % 60)/60
        giay %= 60
    else:
        gio = (giay-giay % 3600)/3600
        phut = ((giay % 3600)-(giay % 3600) % 60)/60
        giay = giay-phut*60-gio*3600

    if gio == 0 and phut == 0:
        return str(giay) + "s"
    elif gio == 0:
        return str(phut) + "m" + str(giay) + "s"
    else:
        return str(gio) + "h" + str(phut) + "m" + str(giay) + "s"
