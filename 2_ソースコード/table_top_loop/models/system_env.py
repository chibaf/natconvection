class SystemEnv:
    """システム環境情報の管理"""

    def __init__(self, param_env):
        self.__gravity = param_env['gravity']
        self.__initial_degree = param_env['initial_degree']
        self.__kinetic_viscosity = param_env['kinetic_viscosity']

    @property
    def gravity(self):
        return self.__gravity

    @property
    def initial_degree(self):
        return self.__initial_degree

    @property
    def kinetic_viscosity(self):
        return self.__kinetic_viscosity
