import random
import time
import numpy as np

class Scheduler(object):
    def __init__(self, name="Standard"):
        self.name = name
        self.wave_list = None
        self.finished = None  # 记录已经完成的任务
        self.ptr_list = None  # 记录每一个任务进行到哪一个时间块了
        self.execution_list = None  # 记录每一个时间点执行的任务

    def insert_waves(self, wave_list):
        self.wave_list = wave_list
        self.finished = set()
        self.ptr_list = dict()
        for wave in wave_list:
            self.ptr_list[wave] = 0
        self.execution_list = []

    def simulate(self, n_timeslots, log = False):
        """
        开始仿真过程，对所有的波进行调度
        参数说明：
        - n_timeslots: 需要进行的时间块数量，超过时间块仿真停止
        返回值：每一个波对应的波形图数据（存储在字典里，需要用波的id进行获取）
        """
        if self.wave_list is None:
            raise ValueError("Wave list has not been initialized")

        begin_time = time.time()
        for i in range(n_timeslots):
            self._iterate()
        end_time = time.time()
        if log:
            print(f"Scheduler {self.name} finished ({end_time - begin_time}s).")

        # 输出每一个波对应的波状图数据
        wave_results = dict()
        for wave in self.wave_list:
            wave_results[wave.id] = []
        for i in range(n_timeslots):
            cur_wave = self.execution_list[i]
            for wave in self.wave_list:
                if wave == cur_wave:
                    wave_results[wave.id].append(1)
                else:
                    wave_results[wave.id].append(0)
        return wave_results

    def _iterate(self):
        # 获取所有还需要进行调度且正是处于需要传输的任务中优先级最高的任务
        highest_priority = 10000
        queue = []  # 即将进行调度的波
        idle_waves = []  # 正在执行计算任务的波
        for wave in self.wave_list:
            if wave not in self.finished:  # 这个任务还没有完成
                if wave.time_series[self.ptr_list[wave]]:  # 并且正处于需要调度的状态
                    if wave.get_priority() < highest_priority:
                        queue = [wave]
                        highest_priority = wave.get_priority()
                    if wave.get_priority() == highest_priority:
                        queue.append(wave)
                else:  # 这个任务处于不需要调度的状态，也就是正在执行计算任务
                    idle_waves.append(wave)

        # 现在获得的队列是最高优先级的队列
        # 目前对于所有最高优先级的队列我们随机选择一个进行调度
        if len(queue) > 0:
            executed_wave = random.choice(queue)
            self.execution_list.append(executed_wave)
            self.ptr_list[executed_wave] += 1
            if self.ptr_list[executed_wave] == len(executed_wave.time_series):
                self.finished.add(executed_wave)
        else:
            self.execution_list.append(None)
        # 对于处在idle列表的任务，同样往后步进一个时间块
        for wave in idle_waves:
            self.ptr_list[wave] += 1

        pass