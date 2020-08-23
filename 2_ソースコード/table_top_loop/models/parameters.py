import json

from ..log_operator import LogOperator
from .system_env import SystemEnv


class Parameters:
    """パラメータファイルのロードと各オブジェクトへの割り当て."""

    def __init__(self):
        with open('loop_param.json') as p:
            param = json.load(p)

        self.__system_env = SystemEnv(param['system_env'])
        self.__system_config = param['system_config']
        self.__system_devices = param['system_devices']
        self.__loop_config = param['loop_config']
        self.__log_operator = LogOperator(param['log_config'], self.__system_env)

    @property
    def system_env(self):
        return self.__system_env

    @property
    def system_config(self):
        return self.__system_config

    @property
    def system_devices(self):
        return self.__system_devices

    @property
    def loop_config(self):
        return self.__loop_config

    @property
    def log_operator(self):
        return self.__log_operator
