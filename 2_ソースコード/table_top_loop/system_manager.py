from copy import deepcopy
from itertools import chain

from .degree import Degree
from .models.core import Core
from .models.heat_exchanger import HeatExchanger
from .models.pipe import Pipe
from .models.pump import Pump


class SystemManager:
    """
    システム全体の情報管理とシステム操作の提供
    【現状の前提】
    ・炉心、ポンプ、HEXはシステムに各1つ
    ・分岐なし
    """

    def __init__(self, param_system_config, param_system_devices, system_env, target_degree):
        self.env = system_env
        self.out_volume_persec = 0 # 現在の系内流量

        # 接続情報をインスタンス化しておく
        self.__device_connections = [DeviceConnect(cn['root'], cn['dist']) for cn in param_system_config['device_connections']]

        self.__core = [Core(self.env, c) for c in param_system_devices['core']]
        self.__pipe = [Pipe(self.env, p) for p in param_system_devices['pipe']]
        self.__pump = [Pump(self.env, p) for p in param_system_devices['pump']]
        self.__heat_exchanger = [HeatExchanger(self.env, h, target_degree)
                                 for h in param_system_devices['heat_exchanger']]

        self.__devices = list(chain.from_iterable([self.__core, self.__pipe, self.__pump, self.__heat_exchanger]))

        self.__elapsed_time = 0

    @property
    def device_connections(self):
        return self.__device_connections

    @property
    def core(self):
        return self.__core[0]

    @property
    def pipe(self):
        return self.__pipe

    @property
    def pump(self):
        return self.__pump[0]

    @property
    def heat_exchanger(self):
        return self.__heat_exchanger[0]

    @property
    def devices(self):
        return self.__devices

    @property
    def elapsed_time(self):
        return self.__elapsed_time

    @property
    def next_device_of_pump(self):
        return self.next_devices(self.pump.id)[0]

    @property
    def previous_device_of_pump(self):
        return self.previous_devices(self.pump.id)[0]

    def next_devices(self, device_id):
        dist_ids = [d.dist for d in self.device_connections if d.root == device_id]
        dvs = [dv for dv in self.devices if dv.id in dist_ids]
        return dvs

    def previous_devices(self, device_id):
        root_ids = [d.root for d in self.device_connections if d.dist == device_id]
        dvs = [dv for dv in self.devices if dv.id in root_ids]
        return dvs

    def move_system(self, delta_pressure_driven_pump, out_volume_persec, heat_energy_persec, timespan):
        # 経過時間更新
        self.__elapsed_time += timespan
        self.__update_timespan(timespan)

        # ポンプデータ更新
        self.pump.out_volume_persec = out_volume_persec
        self.__update_running_volume(self.pump.out_volume * timespan)

        # 質量移動
        self.__move_mass()

        # 熱投入 TODO ポンプの熱投入未実装
        self.__input_heat(heat_energy_persec * timespan)

        # 系内圧力計算
        self.__compute_pressure_in_system(delta_pressure_driven_pump)

    def __update_timespan(self, timespan):
        for d in self.devices:
            d.timespan = timespan

    def __update_running_volume(self, running_volume):
        self.pump.delta_volume_passing_boundary = running_volume
        self.next_device_of_pump.delta_volume_passing_boundary = running_volume
        self.__set_vol_recursive(self.next_devices(self.next_device_of_pump.id)[0])

    def __set_vol_recursive(self, d):
        if(d.id == self.pump.id):
            return
        d.delta_volume_passing_boundary = self.previous_devices(d.id)[0].delta_volume_passing_boundary
        self.__set_vol_recursive(self.next_devices(d.id)[0])

    def __move_mass(self):
        for d in self.devices:
            d.delta_mass_boundary = d.delta_volume_passing_boundary * self.previous_devices(d.id)[0].density
        for d in self.devices:
            d.mass += d.delta_mass_boundary
            d.mass -= self.next_devices(d.id)[0].delta_mass_boundary

    def __input_heat(self, heat_energy):
        self.core.core_heat_energy = heat_energy

        for d in self.devices:
            d.delta_heat_energy_external = d.delta_heat_energy_wall + d.core_heat_energy + \
                    d.hex_heat_energy + d.pump_heat_energy

        for d in self.devices:
            d.delta_heat_energy_boundary = (d.delta_volume_passing_boundary / \
                self.previous_devices(d.id)[0].volume) * self.previous_devices(d.id)[0].heat_energy

        for d in self.devices:
            d.heat_energy += d.delta_heat_energy_boundary + d.delta_heat_energy_external

        self.__update_heat_energy_recursive(self.pump)

        for d in self.devices:
            d.degree = Degree(d.heat_energy / (d.volume * d.density * d.cp_heat))
            d.density = d.calc_density(d.degree_kelvin)
            d.heat_energy_out -= d.delta_heat_energy_wall
            d.degree_out = Degree(d.heat_energy_out / d.heat_continent)

    def __update_heat_energy_recursive(self, d):
        next_d = self.next_devices(d.id)[0]
        d.heat_energy -= next_d.delta_heat_energy_boundary
        if(d.id == self.previous_device_of_pump.id):
            return
        self.__update_heat_energy_recursive(next_d)

    def __compute_pressure_in_system(self, delta_pressure_driven_pump):
        for d in self.devices:
            pre_d = self.previous_devices(d.id)[0]
            delta_head_gravity = -d.density * (self.env.gravity * (d.inlet_z - pre_d.inlet_z))
            delta_pressure_boundary = -((1/2) * d.density * d.velocity ** 2 - (1/2) * pre_d.density * pre_d.velocity ** 2)
            delta_pressure = pre_d.delta_pressure_by_drug_laminar + delta_head_gravity + delta_pressure_boundary
            d.delta_pressure = delta_pressure

        # 各デバイス圧力
        # ポンプの次は個別に指定
        con_pump = self.next_device_of_pump
        con_pump.phuw = delta_pressure_driven_pump
        self.__set_pressure_recursive(self.next_devices(con_pump.id)[0])
                
    def __set_pressure_recursive(self, d):
        if(d.id == self.next_device_of_pump.id):
            return
        d.phuw = self.previous_devices(d.id)[0].phuw + d.delta_pressure
        self.__set_pressure_recursive(self.next_devices(d.id)[0])

    def convergence_pressure(self, driven_by_pump, input_heat, timespan):
        """
        現在の系をコピーし、流量の最小・最大それぞれでループを仮に進め、収束した圧力を得る
        """
        pump_out_max = 0.1
        pump_out_min = 1e-8

        system_max = self.copy()
        system_min = self.copy()
        
        out_volume_max = pump_out_max
        out_volume_min = pump_out_min

        system_max.move_system(driven_by_pump, pump_out_max, input_heat, timespan)
        system_min.move_system(driven_by_pump, pump_out_min, input_heat, timespan)
        
        pressure_min = system_min.pump.phuw
        pressure_max = system_max.pump.phuw

        self.out_volume_persec = out_volume_max

        # 収束ループパラメータ
        iter_max = 100
        eps = 1e-3

        for i in range(0, iter_max):
            if(abs(pressure_max) < eps):
                return
            system_nextpoint = self.copy()
            out_volume_nextpoint = out_volume_max - pressure_max * (out_volume_max - out_volume_min) / (pressure_max - pressure_min)
            system_nextpoint.move_system(driven_by_pump, out_volume_nextpoint, input_heat, timespan)
            pressure_nextpoint = system_nextpoint.pump.phuw

            if(pressure_nextpoint >= 0):
                out_volume_min = out_volume_max
                out_volume_max = out_volume_nextpoint
                pressure_min = pressure_max
                pressure_max = pressure_nextpoint
            else:
                out_volume_max = out_volume_min
                out_volume_min = out_volume_nextpoint
                pressure_max = pressure_min
                pressure_min = pressure_nextpoint
                
            self.out_volume_persec = out_volume_nextpoint

    def copy(self):
        return deepcopy(self)

class DeviceConnect:
    '''
    システム内デバイス接続情報を管理
    '''
    def __init__(self, root, dist):
        self.root = root
        self.dist = dist
