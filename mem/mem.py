"""
D：忆阻器的总长度，默认值为10纳米（即10 ** -9米）。
w_0：掺杂区的初始长度，默认为忆阻器总长度的一半。
R_on：忆阻器被掺杂时的电阻值，默认值为16千欧姆。
R_off：忆阻器未掺杂时的电阻值，默认值为100欧姆。
mobility_u：掺杂物的迁移率，默认为10 ** -14 cm²/V·s。
polarity_n：决定掺杂区是否扩展或收缩的极性参数，正值表示扩展。
flux_history：用于存储历史通量的变量，初始值为0。
"""
import numpy as np

class mem(object):
    def __init__(self,
                 D = 10,
                 R_ON = 16000,
                 R_OFF = 100,
                 mobility_u = 0.1,
                 polarity_n = 1,
                 flux_history = 0,
                 p = 10):


        self.D = D
        self.R_ON = R_ON
        self.R_OFF = R_OFF
        self.mobility_u = mobility_u
        self.polarity_n = polarity_n
        self.flux_history = flux_history
        self.p = p



    # 定义常量
    mu_D = 1e-10  # 掺杂物迁移率，单位 cm²/V·s
    R_ON = 1e3  # 完全掺杂忆阻器电阻，单位欧姆
    D = 10e-9  # 忆阻器长度，单位 m
    eta = 1  # 极性因子，+1 表示扩展，-1 表示收缩
    # p = 10  # 窗口函数参数

    # 窗口函数
    def window_function(self, x):
        return 1 - (2 * x - 1) ** (2 * self.p)

    # 非线性掺杂漂移模型
    def dw_dt(self, w, i):
        x = w / self.D
        return self.polarity_n * (self.mobility_u * self.R_ON / self.D) * i * self.window_function(x)

    #------------------#

    def calculate_fixed_parameters(self):
        self.Q_0 = (self.D ** 2) / (self.mobility_u * self.R_on)
        self.R_delta = self.R_off - self.R_on
        self.R_0 = self.R_on * (self.w_0 / self.D) + self.R_off * (1 - self.w_0 / self.D)

    # Getter functions
    def get_current(self):
        return self.current

    def get_charge(self):
        return self.charge

    def get_flux(self):
        return self.flux

    def get_resistance(self):
        return self.resistance

class ideal_memristor(object):

    # Initialize the ideal memristor with paramters to be used
    def __init__(self, D=10 ** -9, w_0=0.5 * 10 ** -9, R_on=16000, R_off=100,
                 mobility_u=10 ** -14, polarity_n=+1):
        self.D = D
        self.w_0 = w_0
        self.R_off = R_off
        self.R_on = R_on
        self.mobility_u = mobility_u
        self.polarity_n = polarity_n
        self.flux_history = 0

        # print(self.D, self.w_0,self.R_off, self.mobility_u)

    # Calculate parameters which are not time varying
    def calculate_fixed_parameters(self):
        self.Q_0 = (self.D ** 2) / (self.mobility_u * self.R_on)
        self.R_delta = self.R_off - self.R_on
        self.R_0 = self.R_on * (self.w_0 / self.D) + self.R_off * (1 - self.w_0 / self.D)

    # Calculate time variable paramters
    def calculate_time_variable_parameters(self, flux):
        self.flux = self.flux_history + flux
        self.drift_factor = (2 * self.polarity_n * self.R_delta * self.flux) / \
                            (self.Q_0 * (self.R_0 ** 2))

    # Calculate current through memristor
    def calculate_current(self, voltage):
        self.current = (voltage / self.R_0) / ((1 - self.drift_factor) ** 0.5)
        self.resistance = self.R_0 * ((1 - self.drift_factor) ** 0.5)

        # Calculate charge through Memristor

    def calculate_charge(self):
        self.charge = ((self.Q_0 * self.R_0) / self.R_delta) * \
                      (1 - (1 - self.drift_factor) ** 0.5)

    # Update flux history
    def save_flux_history(self):
        self.flux_history = self.flux

    # Getter functions
    def get_current(self):
        return self.current

    def get_charge(self):
        return self.charge

    def get_flux(self):
        return self.flux

    def get_resistance(self):
        return self.resistance

# End of Ideal Memristor class definition











