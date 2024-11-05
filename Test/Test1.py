import numpy as np

# 定义常量
mu_D = 1e-10  # 掺杂物迁移率，单位 cm²/V·s
R_ON = 1e3  # 完全掺杂忆阻器电阻，单位欧姆
D = 10e-9  # 忆阻器长度，单位 m
eta = 1  # 极性因子，+1 表示扩展，-1 表示收缩
p = 10  # 窗口函数参数


# 窗口函数
def window_function(x, p):
    return 1 - (2 * x - 1) ** (2 * p)


# 非线性掺杂漂移模型
def dw_dt(w, i, p):
    x = w / D
    return eta * (mu_D * R_ON / D) * i * window_function(x, p)


# 时间演化过程
def simulate_memristor(i_t, dt, steps):
    w = D / 2  # 初始掺杂区域位置，设置为忆阻器长度的一半
    w_values = [w]

    for i in range(steps):
        # 电流值
        i = i_t[i]

        # 计算dw/dt
        dw = dw_dt(w, i, p)

        # 更新w值
        w += dw * dt
        w_values.append(w)

    return np.array(w_values)


# 示例电流输入（这里假设一个恒定电流输入）
i_t = np.ones(1000) * 1e-6  # 电流为 1 µA
dt = 1e-6  # 时间步长 1 µs
steps = len(i_t)  # 步数

# 运行模拟
w_values = simulate_memristor(i_t, dt, steps)

# 可视化结果
import matplotlib.pyplot as plt

plt.plot(w_values)
plt.xlabel("Time steps")
plt.ylabel("Doped region width (w)")
plt.show()
