from .app_exception import AppException
class Degree:
    """
    温度管理クラス
    """

    def __init__(self, degree_kelvin):
        self.__kelvin = degree_kelvin
        self.kelvin = degree_kelvin

    @property
    def degree_celsius(self):
        return self.kelvin - 273.15

    @property
    def kelvin(self):
        return self.__kelvin

    @kelvin.setter
    def kelvin(self, value):
        if value < 0:
            tempt_ex = AppException(f'invalid tempature. kelvin:{value}')
            raise(tempt_ex)
        self.__kelvin = value
