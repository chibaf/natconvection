from numpy import pi

from .device_base import DeviceBase


class Pump(DeviceBase):
    def __init__(self, env, param_pump):
        """ポンプクラス."""
        super().__init__(env, param_pump['id'], 'pump', param_pump)
        self.__vertical_length = param_pump['vertical_length']
        self.__horizontal_length = param_pump['horizontal_length']
        self.__pump_volume = param_pump['pump_volume']
        self.__impeller = param_pump['impeller']
        self.__heat_conductivity = param_pump['heat_conductivity']
        self.__out_volume_persec_plus = param_pump['out_volume_persec_plus']
        self.__out_volume_persec_minus = param_pump['out_volume_persec_minus']
        self.__specific_heat = param_pump['specific_heat']
        self.__thickness = param_pump['thickness']

        self.out_volume_persec = 0
        self.mass = self.density * self.volume
        self.heat_energy = self.volume * self.density * self.cp_heat * self.degree_kelvin
        self.heat_energy_out = self.heat_continent * self.degree_out_kelvin

    @property
    def heat_conductivity(self):
        return self.calcVal(self.__heat_conductivity)

    @property
    def out_volume_persec_plus(self):
        return self.__out_volume_persec_plus

    @property
    def out_volume_persec_minus(self):
        return self.__out_volume_persec_minus

    @property
    def pump_volume(self):
        return self.calcVal(self.__pump_volume)

    @property
    def vertical_length(self):
        return self.calcVal(self.__vertical_length)

    @property
    def horizontal_length(self):
        return self.calcVal(self.__horizontal_length)

    @property
    def impeller(self):
        return self.calcVal(self.__impeller)

    @property
    def specific_heat(self):
        return self.calcVal(self.__specific_heat)

    @property
    def thickness(self):
        return self.calcVal(self.__thickness)

    @property
    def heat_continent(self):
        return 2 * 1e5  # TODO 元コードに正確ではないとメモあり

    @property
    def volume(self):
        return self.calcVal(self.__pump_volume)

    @property
    def area_l_end_boundary(self):
        return self.dia ** 2 * pi / 4

    @property
    def area_r_end_boundary(self):
        return self.area_l_end_boundary

    @property
    def side_area(self):
        return self.dia * pi * 2 * self.length

    @property
    def out_volume(self):
        return self.out_volume_persec * self.timespan
