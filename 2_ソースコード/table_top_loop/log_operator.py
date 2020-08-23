from itertools import chain
import numpy as np
from matplotlib import pyplot as plt
from datetime import datetime

class LogOperator:
    """
    ロギング管理
    """

    def __init__(self, param_log, system_env):
        self.__outfile = param_log['outfile']
        self.__env = system_env
        self.visualizer = Visualizer(self.__outfile)
        self.save_path = f'{self.__outfile}\\ttl_log_{datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}.log'
        self.save_fig_path = f'{self.__outfile}\\ttl_graph_{datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}'

    @property
    def outfile(self):
        return self.__outfile

    def write(self, input_heat, pump_pressure, core, pump, heat_exchanger, pipes, next_of_pump, flow, time_point):
        log_thispoint = f'''
            Elapsed Time(s)      : {time_point}
            Segment After Pump Info
            Diamter              : {next_of_pump.dia}
            Length               : {next_of_pump.length}
            Kinetic Viscosity    : {self.__env.kinetic_viscosity}
            Degree(C)            : {next_of_pump.degree_celsius}
            Degree(K)            : {next_of_pump.degree_kelvin}
            Pressure Pump Head   : {next_of_pump.phuw}
            Flow Rate            : {flow}
            HEX Heat Energy Wall : {heat_exchanger.delta_heat_energy_wall}
            --------------------------------------------

        '''
        print(log_thispoint)
        with open(self.save_path, mode='a') as f:
            f.write(log_thispoint)


    def show_graph(self, cores, pumps, heat_exchangers, pipes, timestep, drow_span):
        self.visualizer.plot(cores, pumps, heat_exchangers, pipes, timestep, drow_span)

    def save_graph(self):
        self.visualizer.save_fig(self.save_fig_path)

class Visualizer:
    """
    グラフ表示
    """

    def __init__(self, outpath):
        self.outpath = outpath
        self.__fig = plt.figure(1, figsize=(10, 7))
        self.__ax_deg = self.__fig.add_subplot(311)
        self.__ax_dens = self.__fig.add_subplot(312)
        self.__ax_vel = self.__fig.add_subplot(313)

        self.__min_deg = 1000
        self.__max_deg = 0
        self.__min_den = 5000
        self.__max_den = 0
        self.__min_vel = 0
        self.__max_vel = 0

    def plot(self, core, pump, heat_exchanger, pipes, time_point, drow_span):
        devices = [[core], [pump], [heat_exchanger], pipes]

        segments = sorted(list(chain.from_iterable(devices)), key=lambda s: s.id)

        segment_count = len(segments)
        xx = np.array(list(map(lambda s: s.id, segments)))

        segment_degrees = np.array(list(map(lambda s: s.degree_kelvin, segments)))
        segment_densities = np.array(list(map(lambda s: s.density, segments)))
        segment_velocities = np.array(list(map(lambda s: s.velocity, segments)))
        # 描画範囲更新
        self.__min_deg = min([self.__min_deg, np.min(segment_degrees) - 10])
        self.__max_deg = max([self.__max_deg, np.max(segment_degrees) + 10])
        self.__min_den = min([self.__min_den, np.min(segment_densities) - 10])
        self.__max_den = max([self.__max_den, np.max(segment_densities) + 10])
        self.__min_vel = min([self.__min_vel, np.min(segment_velocities) - 0.1])
        self.__max_vel = max([self.__max_vel, np.max(segment_velocities) + 0.1])

        self.__fig.suptitle(f'Elasped Time:{time_point}(s)   Drow Span:{drow_span}(s)')

        self.__ax_deg.set_title('TTL code verification output')  # Title of plot

        self.__ax_deg.set_xlim(-1, segment_count)
        self.__ax_deg.set_ylim(self.__min_deg, self.__max_deg)
        self.__ax_deg.set_ylabel('Fluid Temperature(K)')      # label of y-axis

        self.__ax_dens.set_xlim(-1, segment_count)
        self.__ax_dens.set_ylim(self.__min_den, self.__max_den)  # (-50,150) #(0,70)
        self.__ax_dens.set_ylabel('Fluid Density')      # label of y-axis

        self.__ax_vel.set_xlim(-1, segment_count)
        self.__ax_vel.set_ylim(self.__min_vel, self.__max_vel)  # (-50,150) #(0,70)
        self.__ax_vel.set_xticks(xx)
        self.__ax_vel.set_xticklabels(list(map(lambda s: f'{s.kind}_{s.id}', segments)), rotation=70)
        self.__ax_vel.set_ylabel('Fluid velocity')      # label of y-axis

        plt.pause(0.01)
        self.__ax_deg.plot(xx, segment_degrees, label='salt degree(K)')
        plt.pause(0.01)
        self.__ax_dens.plot(xx, segment_densities, label='density')
        plt.pause(0.01)
        self.__ax_vel.plot(xx, segment_velocities, label='velocity')

    def save_fig(self, fname):
        plt.savefig(fname)