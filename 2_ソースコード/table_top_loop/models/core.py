from numpy import pi, sqrt

from .device_base import DeviceBase


class Core(DeviceBase):
    """炉心クラス."""

    def __init__(self, env, param_core):
        super().__init__(env, param_core['id'], 'core', param_core)
        self.__length = param_core['length']
        self.__inside_diamiter = param_core['inside_diamiter']
        self.__heat_conductivity = param_core['heat_conductivity']
        self.__fuel_channel_number = param_core['fuel_channel_number']
        self.__channel_length_of_horizontal = param_core['channel_length_of_horizontal']
        self.__channel_length_of_vertical = param_core['channel_length_of_vertical']
        self.__specific_heat = param_core['specific_heat']
        self.__thickness = param_core['thickness']

        self.mass = self.density * self.volume
        self.delta_heat_energy = 0
        self.heat_energy = self.volume * self.density * self.cp_heat * self.degree_kelvin
        self.heat_energy_out = self.heat_continent * self.degree_out_kelvin

    @property
    def inside_diamiter(self):
        return self.calcVal(self.__inside_diamiter)

    @property
    def heat_conductivity(self):
        return self.calcVal(self.__heat_conductivity)

    @property
    def dia(self):
        return 2*sqrt(self.channel_length_of_horizontal * self.channel_length_of_vertical / pi)

    @property
    def fuel_channel_number(self):
        return self.__fuel_channel_number

    @property
    def channel_length_of_horizontal(self):
        return self.calcVal(self.__channel_length_of_horizontal)

    @property
    def channel_length_of_vertical(self):
        return self.calcVal(self.__channel_length_of_vertical)

    @property
    def specific_heat(self):
        return self.calcVal(self.__specific_heat)

    @property
    def heat_continent(self):
        return (self.inside_diamiter ** 2 * pi / 4 * self.length - self.volume) * self.specific_heat

    @property
    def thickness(self):
        return self.calcVal(self.__thickness)

    @property
    def volume(self):
        return self.area_l_end_boundary * self.length

    @property
    def area_l_end_boundary(self):
        return self.fuel_channel_number * self.channel_length_of_horizontal * self.channel_length_of_vertical

    @property
    def area_r_end_boundary(self):
        return self.area_l_end_boundary

    @property
    def side_area(self):
        return 2 * self.fuel_channel_number * self.channel_length_of_horizontal + \
            self.channel_length_of_vertical * self.length
