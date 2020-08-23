from abc import ABC, abstractproperty
from numpy import pi, sqrt
from ..degree import Degree

class DeviceBase(ABC):
    """システム構成部品ベースクラス."""

    def __init__(self, env, id, kind, param_device):
        self.env = env

        self.__id = id
        self.__kind = kind
        self.__degree = Degree(self.env.initial_degree)
        self.__degree_out = Degree(self.env.initial_degree)
        self.__velocity = 0
        self.__heat_energy = 0
        self.__heat_energy_out = 0
        self.__density = self.calc_density(self.__degree.kelvin)

        self.__length = param_device['length']
        self.__inlet_x = param_device['inlet_x']
        self.__inlet_y = param_device['inlet_y']
        self.__inlet_z = param_device['inlet_z']
        self.__outlet_x = param_device['outlet_x']
        self.__outlet_y = param_device['outlet_y']
        self.__outlet_z = param_device['outlet_z']
        self.__dia = param_device['dia']

        self.__timespan = 0

        self.phuw = 0  # TODO これもなんの略語だか知りたい

        self.core_heat_energy = 0
        self.pump_heat_energy = 0
        self.hex_heat_energy = 0

        self.delta_volume_passing_boundary = 0
        self.delta_heat_energy_boundary = 0
        self.delta_heat_energy_external = 0
        self.delta_pressure = 0
        self.__mass = 0
        self.delta_mass_boundary = 0

    @property
    def id(self):
        return self.__id

    @property
    def kind(self):
        return self.__kind

    @property
    def timespan(self):
        return self.__timespan

    @timespan.setter
    def timespan(self, time):
        self.__timespan = time

    @property
    def length(self):
        return self.calcVal(self.__length)

    @property
    def inlet_x(self):
        return self.calcVal(self.__inlet_x)

    @property
    def inlet_y(self):
        return self.calcVal(self.__inlet_y)

    @property
    def inlet_z(self):
        return self.calcVal(self.__inlet_z)

    @property
    def outlet_x(self):
        return self.calcVal(self.__outlet_x)

    @property
    def outlet_y(self):
        return self.calcVal(self.__outlet_y)

    @property
    def outlet_z(self):
        return self.calcVal(self.__outlet_z)

    @property
    def dia(self):
        return self.calcVal(self.__dia)

    @property
    def degree(self):
        return self.__degree

    @property
    def degree_celsius(self):
        return self.__degree.degree_celsius

    @property
    def degree_kelvin(self):
        return self.__degree.kelvin

    @degree.setter
    def degree(self, degree_obj):
        self.__degree = degree_obj

    # TODO stの意味がわからないのでもっといい名前にする
    @property
    def degree_out(self):
        return self.__degree_out

    @property
    def degree_out_celsius(self):
        return self.__degree_out.degree_celsius

    @property
    def degree_out_kelvin(self):
        return self.__degree_out.kelvin

    @degree_out.setter
    def degree_out(self, degree_obj):
        self.__degree_out = degree_obj

    @property
    def density(self):
        return self.__density

    @density.setter
    def density(self, density_val):
        self.__density = density_val

    @property
    def mass(self):
        return self.__mass

    @mass.setter
    def mass(self, massValue):
        self.__mass = massValue

    @property
    def velocity(self):
        __vel = 0 if self.timespan == 0 else self.delta_volume_passing_boundary / self.area_l_end_boundary / self.timespan
        return __vel

    @property
    def cp_heat(self):
        return 4683  # 実際は関数になるらしいので、取り敢えずパラメータファイルに持たせずリテラルで持つ

    @property
    def heat_energy(self):
        return self.__heat_energy

    @heat_energy.setter
    def heat_energy(self, heat_energy_val):
        self.__heat_energy = heat_energy_val

    @property
    def heat_energy_out(self):
        return self.__heat_energy_out

    @heat_energy_out.setter
    def heat_energy_out(self, heat_energy_out_val):
        self.__heat_energy_out = heat_energy_out_val

    @property
    def delta_heat_energy_wall(self):
        return -1 * self.heat_conductivity * (self.degree.kelvin - self.degree_out.kelvin) / self.thickness * self.side_area * self.timespan

    @property
    def delta_pressure_by_drug_laminar(self):
        return -32 * self.env.kinetic_viscosity * self.length * self.density * self.velocity / self.dia ** 2

    @abstractproperty
    def heat_conductivity(self):
        pass

    @abstractproperty
    def heat_continent(self):
        pass

    @abstractproperty
    def thickness(self):
        pass

    @abstractproperty
    def volume(self):
        pass

    @abstractproperty
    def area_l_end_boundary(self):
        pass

    @abstractproperty
    def area_r_end_boundary(self):
        pass

    @abstractproperty
    def side_area(self):
        pass

    @staticmethod
    def calc_density(kelvin):
        return 2413.03 - 0.4884 * kelvin

    @staticmethod
    def calcVal(param_value):
        if(type(param_value) is str):
            return eval(param_value)
        else:
            return param_value
