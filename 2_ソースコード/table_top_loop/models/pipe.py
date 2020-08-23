from numpy import pi

from .device_base import DeviceBase


class Pipe(DeviceBase):
    def __init__(self, env, param_pipe):
        """パイプクラス."""
        super().__init__(env, param_pipe['id'], 'pipe', param_pipe)
        self.__outside_diamiter = param_pipe['outside_diamiter']
        self.__heat_conductivity = param_pipe['heat_conductivity']
        self.__specific_heat = param_pipe['specific_heat']
        self.__thickness = param_pipe['thickness']

        self.__block_rate = 1

        self.mass = self.density * self.volume
        self.heat_energy = self.volume * self.density * self.cp_heat * self.degree_kelvin
        self.heat_energy_out = self.heat_continent * self.degree_out_kelvin


    @property
    def heat_conductivity(self):
        return self.calcVal(self.__heat_conductivity)

    @property
    def outside_diamiter(self):
        return self.calcVal(self.__outside_diamiter)

    @property
    def specific_heat(self):
        return self.calcVal(self.__specific_heat)

    @property
    def thickness(self):
        return self.calcVal(self.__thickness)

    @property
    def heat_continent(self):
        return (self.outside_diamiter ** 2 - self.dia ** 2) * pi / 4 * self.length * self.specific_heat

    @property
    def volume(self):
        return self.area_l_end_boundary * self.length

    @property
    def area_l_end_boundary(self):
        return self.dia ** 2 * pi / 4 * self.block_rate

    @property
    def area_r_end_boundary(self):
        return self.area_l_end_boundary

    @property
    def side_area(self):
        return self.dia * self.length

    @property
    def block_rate(self):
        return self.__block_rate

    @block_rate.setter
    def block_rate(self, rate):
        self.__block_rate = rate
