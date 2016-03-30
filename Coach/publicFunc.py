# coding:utf-8
def get_all_interval(begin_time, end_time):
    '''
    返回开始时间和结束时间的间隔，单位：s
    '''
    hour_interval = (end_time.hour - begin_time.hour) * 60 * 60
    minute_interval = (end_time.minute - begin_time.minute) * 60
    second_interval = end_time.second - begin_time.second
    return hour_interval + minute_interval + second_interval
