from .app_exception import AppException
class ErrorManager:
  '''
  ループ実行時の異常発生を管理する
  '''
  def __init__(self, devices, error_setting):
    self.devices = devices
    self.errors = []
    for err in error_setting:
      self.errors.append(ErrorSetting(err))
  
  def maybe_error_occurs(self, time_point):
    err_range = list(filter(lambda e: e.time <= time_point and not e.occurred, self.errors))
    if(len(err_range) < 1):
      # エラー未発生
      return
    for err in err_range:
      err.execute(self.devices)

class ErrorSetting:
  '''
  ・異常の設定内容を管理する
  ・設定内容をデバイスに反映する
  '''
  def __init__(self, setting):
    self.type = setting['type']
    self.point_id = setting['point_id']
    self.time = setting['time']
    self.enable = setting['enable']

    self.occurred = False

    if(self.type == ErrorType.PIPE_BLOCK.value):
      self.block_rate = setting['block_rate_of_l_end_area']

  def execute(self, devices):
    if(not eval(self.enable)):
      self.occurred = True
      return
    if(self.type == ErrorType.PIPE_BLOCK.value):
      self.execute_block(devices)
      self.occurred = True

  def execute_block(self, devices):
    pipes = list(filter(lambda p: p.id == self.point_id, devices))
    if(len(pipes) != 1):
      raise AppException(f'Error Target Device is Not Exists. id={self.point_id}')
    pipe = pipes[0]
    pipe.block_rate = self.block_rate
    

from enum import Enum
class ErrorType(Enum):
  '''
  異常の種類を管理する（列挙体）
  '''
  PIPE_BLOCK = "pipe_block"
