import json
import os

eqt_dict = {'a': [], 'b': []}
counter = 0

"""
    返回最近一次上传文件内包含的地震数据
"""


def get_file_list():
    global counter
    if counter % 2 == 1:
        eqt_list = eqt_dict['a']
    else:
        eqt_list = eqt_dict['b']

    return [earthquake.json_earthquake() for earthquake in eqt_list]


"""
    从给定的路径读取地震数据文件，并返回地震object列表，同时标明该地震文件是A/B文件
"""


def read_eqt(filename):
    global counter
    earthquakes = []
    for line in open(filename, 'r', encoding='gbk'):
        earthquakes.append(Earthquake(line))
    if counter % 2 == 0:
        eqt_dict['a'] = earthquakes
    else:
        eqt_dict['b'] = earthquakes
    counter += 1
    return earthquakes


def get_required_cases(ymdOneLimit=None, abOneSelect=None, disOneLimit=None, jingweiLimit=None):
    # TODO: 将所有earthquake中的过滤器函数整合
    pass


# TODO: 给定的数据中无法在地震发生后A/B表内筛选特定距离范围内发生的地震

class Earthquake:
    def __init__(self, info):
        data = info.split()
        self.year = int(data[0])
        self.month = int(data[1])
        self.day = int(data[2])
        self.time = data[3]
        self.latitude = float(data[4])
        self.longitude = float(data[5])
        self.level = float(data[6])
        self.depth = float(data[7])
        if len(data) == 8:
            #如果没有新的地点，就把它设定为null
            self.position = "null"
        else:
            self.position = data[8]

    """
        将Earthquake object转化为json数据格式
    """

    def json_earthquake(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4, ensure_ascii=False)

    """
        判断某个地震是否在指定地震发生后发生
        eqt: 指定的地震
    """

    def is_after(self, eqt):
        eqt_time = list(map(int, eqt.time.split('-')))
        curr_time = list(map(int, self.time.split('-')))
        for i in range(len(curr_time)):
            if curr_time[i] - eqt_time[i] < 0:
                return False
        return True

    """
        判断某个地震是否在地震发生后的某个特定时间范围内
        ymdOneLimit: 包含时间范围【年，月，日】的列表
        eqt: 需要判断的地震object
    """

    def within_time_range(self, ymdOneLimit, start_eqt):
        if not self.is_after(start_eqt):
            return False

        start_time = list(map(int, start_eqt.time.split('-')))
        curr_time = list(map(int, self.time.split('-')))
        for i in range(len(curr_time)):
            if ymdOneLimit[i] < curr_time[i] - start_time[i]:
                return False
        return True

    """
        返回（A表中）发生地震某时间范围内，B表内符合条件的地震
        ymdOneLimit: 包含时间范围【年，月，日】的列表
        返回列表中地震数据以json格式返回
    """

    def get_cases_within_time_limit(self, ymdOneLimit, abOneSelect=1):
        eqt_list = eqt_dict['b']
        ret_eqt_list = []
        for eqt in eqt_list:
            if eqt.within_time_range(ymdOneLimit, self):
                ret_eqt_list.append(eqt.json_eqrthquake())
        return ret_eqt_list

    """
        判断某个地震是否在地震发生后某个特定经纬度范围内
        jingweiLimit: 包含经纬度范围【经度最小，经度最大，纬度最小，纬度最大】的列表
        eqt: 需要判断的地震object
    """

    def within_jingwei_range(self, jingweiLimit, start_eqt):
        if not self.is_after(start_eqt):
            return False

        start_longitude = jingweiLimit[0]
        end_longitude = jingweiLimit[1]
        start_latitude = jingweiLimit[2]
        end_latitude = jingweiLimit[3]

        return start_longitude < self.longitude < end_longitude and start_latitude < self.latitude < end_latitude

    """
        返回（A表中）发生地震某时间范围内，A/B表内符合条件的地震
        jingweiLimit: 包含经纬度范围【经度最小，经度最大，纬度最小，纬度最大】的列表
        返回列表中地震数据以json格式返回
    """

    def get_cases_within_jingwei_limit(self, abOneSelect, jingweiLimit):
        if abOneSelect == 0:
            eqt_list = eqt_dict['a']
        elif abOneSelect == 1:
            eqt_list = eqt_dict['b']
        else:
            raise IndexError

        ret_eqt_list = []
        for eqt in eqt_list:
            if eqt.within_jingwei_range(jingweiLimit, self):
                ret_eqt_list.append(eqt.json_eqrthquake())
        return ret_eqt_list
