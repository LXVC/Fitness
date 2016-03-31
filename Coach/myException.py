# coding:utf-8
class EndBeforeBeginError(Exception):
    message = u'结束时间不能早于开始时间!'

    def __init__(self, all_interval):
        Exception.__init__(self)
        self.interval = all_interval

    def __str__(self):
        return repr(self.message)


class StepTooLongError(Exception):
    message = u'时间间隔太长'

    def __init__(self, all_interval, step):
        Exception.__init__(self)
        self.interval = all_interval
        self.step = step

    def __str__(self):
        return repr(self.message)


class isCoverByAcceptedError(Exception):
    message = u'已经接受预约,不能接受新的预约'

    def __init__(self):
        Exception.__init__(self)

    def __str__(self):
        return repr(self.message)