"""
项目的主入口
"""
from Wave import Wave
from Scheduler import Scheduler
from Visualization import plot_multiple_waves
from Visualization import plot_single_wave
if __name__ == '__main__':
    # wave_list = []
    # for i in range(5):
    #     wave = Wave(4, 2, 2, 4, i)
    #     wave.set_priority(i)
    #     wave_list.append(wave)
    #     wave.show_details()

    wave_1 = Wave(4, 2, 2, 10, 0)
    wave_1.set_priority(0)
    wave_2 = Wave(5, 2, 3, 10, 1)
    wave_2.set_priority(1)

    scheduler = Scheduler()
    scheduler.insert_waves([wave_1, wave_2])
    n_timeslots = 50
    wave_results = scheduler.simulate(n_timeslots, True)

    plot_multiple_waves([wave_1, wave_2], wave_results)
    # plot_single_wave(wave_list[0], wave_results[wave_list[0].id])
