from numpy import pi

from .device_base import DeviceBase


class HeatExchanger(DeviceBase):
    """熱交換機（Heat Exchanger）クラス."""

    def __init__(self, env, param_heat_exchanger, target_degree):
        super().__init__(env, param_heat_exchanger['id'], 'heat_exchanger', param_heat_exchanger)
        self.__outside_diamiter = param_heat_exchanger['outside_diamiter']
        self.__inside_diamiter = param_heat_exchanger['inside_diamiter']
        self.__length_of_utube = param_heat_exchanger['length_of_utube']
        self.__utube_number = param_heat_exchanger['utube_number']
        self.__heat_conductivity = param_heat_exchanger['heat_conductivity']
        self.__specific_heat = param_heat_exchanger['specific_heat']
        self.__thickness = param_heat_exchanger['thickness']

        self.__target_degree = target_degree

        self.mass = self.density * self.volume
        self.delta_heat_energy = 0
        self.heat_energy = self.volume * self.density * self.cp_heat * self.degree_kelvin
        self.heat_energy_out = self.heat_continent * self.degree_out_kelvin

    @property
    def heat_conductivity(self):
        return self.calcVal(self.__heat_conductivity)

    @property
    def outside_diamiter(self):
        return self.calcVal(self.__outside_diamiter)

    @property
    def inside_diameter(self):
        return self.calcVal(self.__inside_diamiter)

    @property
    def length_of_utube(self):
        return self.calcVal(self.__length_of_utube)

    @property
    def utube_number(self):
        return self.calcVal(self.__utube_number)

    @property
    def specific_heat(self):
        return self.calcVal(self.__specific_heat)

    @property
    def thickness(self):
        return self.calcVal(self.__thickness)

    @property
    def heat_continent(self):
        return 1e20

    @property
    def volume(self):
        return self.area_l_end_boundary * self.length_of_utube

    @property
    def area_l_end_boundary(self):
        return self.utube_number * self.inside_diameter ** 2 * pi / 4

    @property
    def area_r_end_boundary(self):
        return self.area_l_end_boundary

    @property
    def side_area(self):
        # reach = self.degree_celsius > self.__target_degree.degree_celsius
        # return self.utube_number * self.inside_diameter * pi * self.length_of_utube if reach else 1e-5
        return self.utube_number * self.inside_diameter * pi * self.length_of_utube
