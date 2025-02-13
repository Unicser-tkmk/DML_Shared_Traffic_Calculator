import numpy as np
class Wave(object):
    def __init__(self, period, on_duration, offset, n_periods, id=0):
        """
        传输仿真波，用于仿真某个训练任务的数据传输过程
        参数说明：
        period: 一个周期的时长
        on_duration: 一个周期里用于传输的时间长度
        offset: 一个周期里用于训练模型的时间长度
        n_periods: 本训练任务需要完成的周期数量
        """
        if on_duration + offset != period:
            raise ValueError('on_duration + offset must be equal to period')
        if n_periods < 1:
            raise ValueError('n_periods must be greater than 0')
        self.period = period
        self.on_duration = on_duration
        self.offset = offset
        self.n_periods = n_periods
        self.id = id
        self.time_series = self.generate_time_series()
        self._priority = None  # 私有变量，不允许直接读取

    def generate_time_series(self):
        """生成仿真的波形数据，返回一个numpy数组"""
        # 一个周期的波形
        single_period = np.array([0] * self.offset + [1] * self.on_duration)
        # 复制n_periods次
        time_series = np.tile(single_period, self.n_periods)
        return time_series

    def set_priority(self, priority):
        self._priority = priority

    def get_priority(self):
        if self._priority is None:
            raise ValueError('Priority is not set')
        return self._priority


    def show_details(self):
        print(f"Wave {self.id}: period={self.period}, on_duration={self.on_duration}, offset={self.offset}, n_periods={self.n_periods}, priority={self._priority}.")