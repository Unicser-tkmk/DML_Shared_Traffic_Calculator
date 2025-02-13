import matplotlib.pyplot as plt
import numpy as np
from Wave import Wave
def plot_three_waves(t, T_total, wave1, wave2, modified_wave2):
    # ---------------------------
    # Plotting All Waves in One Figure (Three Subplots)
    # ---------------------------
    fig, axs = plt.subplots(3, 1, figsize=(12, 10), sharex=True)

    # Subplot 1: Wave 1 (Priority)
    axs[0].step(t, wave1, where='post', color='blue')
    axs[0].set_title("Wave 1 (Priority)")
    axs[0].set_ylabel("Signal Level")
    axs[0].set_ylim(-0.2, 1.2)
    axs[0].grid(True)
    axs[0].set_xticks(np.arange(0, T_total + 1, 1))

    # Subplot 2: Original Wave 2
    axs[1].step(t, wave2, where='post', color='green')
    axs[1].set_title("Original Wave 2")
    axs[1].set_ylabel("Signal Level")
    axs[1].set_ylim(-0.2, 1.2)
    axs[1].grid(True)
    axs[1].set_xticks(np.arange(0, T_total + 1, 1))

    # Subplot 3: Modified (Retimed) Wave 2
    axs[2].step(t, modified_wave2, where='post', color='red', linewidth=2)
    axs[2].set_title("Modified (Retimed) Wave 2")
    axs[2].set_xlabel("Time (s)")
    axs[2].set_ylabel("Signal Level")
    axs[2].set_ylim(-0.2, 1.2)
    axs[2].grid(True)
    axs[2].set_xticks(np.arange(0, T_total + 1, 1))

    plt.tight_layout()
    plt.show()


def plot_multiple_waves(wave_list: list, wave_results: dict):
    """
    绘制多条波形，每条波形占一行
    参数：
    - wave_list: 包含多个 Wave 实例的列表
    - wave_results: 字典，键为 Wave 实例的名字，值为其对应的时间序列
    """
    num_waves = len(wave_list)
    T_total = max(len(w) for w in wave_results.values())  # 计算最长的波形时间
    t = np.arange(T_total)

    fig, axs = plt.subplots(num_waves, 1, figsize=(12, 2 * num_waves), sharex=True)

    if num_waves == 1:
        axs = [axs]  # 保证 axs 是列表，即使只有一个子图

    for i, wave in enumerate(wave_list):
        wave_name = f"Wave {wave.id}"
        wave_data = wave_results.get(wave.id, [])
        if not wave_data:
            continue  # 跳过无数据的波形

        axs[i].step(t, wave_data, where='post')
        axs[i].set_title(wave_name)
        axs[i].set_ylabel("Signal Level")
        axs[i].set_ylim(-0.2, 1.2)
        axs[i].grid(True)
        axs[i].set_xticks(np.arange(0, T_total + 1, 1))

    axs[-1].set_xlabel("Time (s)")  # 仅在最后一个子图添加 X 轴标签
    plt.tight_layout()
    plt.show()


def plot_single_wave(wave: Wave, wave_result: list):
    """
    绘制单个波形图
    参数：
    - wave: Wave 实例
    - wave_result: 对应的波形数据列表
    """
    T_total = len(wave_result)
    t = np.arange(T_total)

    plt.figure(figsize=(12, 4))
    plt.step(t, wave_result, where='post', color='blue', linewidth=2)
    plt.title(f"Wave {wave.id}")
    plt.xlabel("Time (s)")
    plt.ylabel("Signal Level")
    plt.ylim(-0.2, 1.2)
    plt.grid(True)
    plt.xticks(np.arange(0, T_total + 1, 1))
    plt.show()