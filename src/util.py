from datetime import time, timedelta
#data_file_name = 'data/1_Poisy-ParcDesGlaisins.txt'
#data_file_name = 'data/2_Piscine-Patinoire_Campus.txt'
def time_between(t1, t2):
    t1 = to_datetime(t1)
    t2 = to_datetime(t2)
    diff = timedelta(hours = t2.hour, minutes= t2.minute) - timedelta(hours = t1.hour, minutes = t1.minute)
    return diff


def add_travel_time(t, travel_time):
    t = to_datetime(t)
    arrival_td = timedelta(hours = t.hour, minutes= t.minute) + timedelta(minutes= travel_time)
    hour = int(arrival_td.total_seconds() // 3600)
    minute = int((arrival_td.total_seconds() % 3600) / 60)
    if minute >= 0 and minute <= 9: minute = f"0{minute}"
    return f"{hour}:{minute}"

def to_datetime(t):
    h, m = t.split(':')
    return time(int(h), int(m))

def read_route_data(data_file_name):
    try:
        with open(data_file_name, 'r', encoding = "UTF-8") as f:
            content = f.read()
    except OSError:
        # 'File not found' error message.
        print("File not found")
        exit()

    def dates2dic(dates):
        dic = {}
        splitted_dates = dates.split("\n")
        #print(splitted_dates)
        for stop_dates in splitted_dates:
            tmp = stop_dates.split(" ")
            dic[tmp[0]] = tmp[1:]
        return dic

    slited_content = content.split("\n\n")
    regular_path = slited_content[0]
    regular_date_go = dates2dic(slited_content[1])
    regular_date_back = dates2dic(slited_content[2])
    we_holidays_path = slited_content[3]
    we_holidays_date_go = dates2dic(slited_content[4])
    we_holidays_date_back = dates2dic(slited_content[5])

    return {
        "slited_content" : slited_content,
        "regular_path" : regular_path,
        "regular_date_go" : regular_date_go,
        "regular_date_back" : regular_date_back,
        "we_holidays_path" : we_holidays_path,
        "we_holidays_date_go" : we_holidays_date_go,
        "we_holidays_date_back" : we_holidays_date_back
    }

