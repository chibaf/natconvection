from .degree import Degree
from .models.parameters import Parameters
from .system_manager import SystemManager
from .error_manager import ErrorManager
from .app_exception import AppException

def start():
    '''
    実際の処理の開始
    ①パラメータロード、各種オブジェクトのインスタンス化
    ②ループ定数リテラルの設定
    ③ループ実行
    '''
    param = Parameters()

    system_env = param.system_env
    
    log_span_iter = 100
    drow_span_iter = 100

    loop_config = LoopConfig(param.loop_config)
    logger = param.log_operator

    system_manager = SystemManager(param.system_config, param.system_devices, system_env, loop_config.target_degree)

    system_error = ErrorManager(system_manager.devices, loop_config.system_error)

    for i in range(0, loop_config.max_iteration):
        time_point = loop_config.interval_second * i
        # 投入熱量取得
        heat_range = list(filter(lambda p: p.time <= time_point, loop_config.heat_input_persec))
        heat_energy_persec = sorted(heat_range, key=lambda x: x.time, reverse=True)[0].energy
        if(heat_energy_persec < 0):
            # 入力温度例外
            raise AppException(f"invalid heat setting. must be positive value, but input {heat_energy_persec}.")
        # ポンプ圧力取得
        pressure_of_pump_range = list(filter(lambda p: p.time <= time_point, loop_config.pressure_of_pump_persec))
        pressure_of_pump = sorted(pressure_of_pump_range, key=lambda x: x.time, reverse=True)[0].pressure
        # 圧力収束
        system_manager.convergence_pressure(pressure_of_pump, heat_energy_persec, loop_config.interval_second)

        system_manager.move_system(pressure_of_pump, system_manager.out_volume_persec, heat_energy_persec, loop_config.interval_second)
        system_error.maybe_error_occurs(time_point)

        if i % log_span_iter == 0:
            logger.write(heat_energy_persec, pressure_of_pump,
                         system_manager.core, system_manager.pump,
                         system_manager.heat_exchanger, system_manager.pipe,
                         system_manager.next_device_of_pump,
                         system_manager.out_volume_persec, time_point)
        if i % drow_span_iter == 0:
            logger.show_graph(system_manager.core, system_manager.pump,
                              system_manager.heat_exchanger, system_manager.pipe, time_point,
                              loop_config.interval_second * drow_span_iter)

    logger.save_graph()
    input('Press Enter key...')


class LoopConfig:
    """
    ループパラメータの管理
    """

    def __init__(self, param_loop):
        self.__max_iteration = param_loop['max_iteration']
        self.__interval_second = param_loop['interval_second']
        self.__target_degree = Degree(param_loop['target_degree'])
        self.__heat_input_persec = param_loop['heat_input_persec']
        self.__pressure_of_pump_persec = param_loop['pressure_of_pump_persec']
        self.__system_error = param_loop['system_error']

    @property
    def max_iteration(self):
        return self.__max_iteration

    @property
    def interval_second(self):
        return self.__interval_second

    @property
    def target_degree(self):
        return self.__target_degree

    @property
    def heat_input_persec(self):
        return [EnergyTimeline(h['time'], h['energy']) for h in self.__heat_input_persec]

    @property
    def pressure_of_pump_persec(self):
        return [PumpPowerTimeline(p['time'], p['pressure']) for p in self.__pressure_of_pump_persec]

    @property
    def system_error(self):
        return self.__system_error


class EnergyTimeline:
    '''
    炉心からの投入熱量データを管理
    '''
    def __init__(self, time, energy):
        self.time = time
        self.energy = energy

class PumpPowerTimeline:
    '''
    ポンプ圧力データを管理
    '''
    def __init__(self, time, pressure):
        self.time = time
        self.pressure = pressure
