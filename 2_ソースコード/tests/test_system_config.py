import json

import pytest

from table_top_loop.models.system_env import SystemEnv
from table_top_loop.system_manager import SystemManager


@pytest.fixture
def sys_manager():
  sys_env = json.loads('''
    { "system_env": {
      "gravity": 9.80665,
      "initial_degree": 15.0,
      "kinetic_viscosity":2.9e-6
    } }
    ''')['system_env']
  sys_cn = json.loads('''
  {
    "system_config": {
      "device_connections": [
        {
          "root": 0,
          "dist": 1
        },
        {
          "root": 1,
          "dist": 2
        },
        {
          "root": 2,
          "dist": 3
        },
        {
          "root": 3,
          "dist": 4
        },
        {
          "root": 4,
          "dist": 0
        }
      ]
    }
  }
  ''')['system_config']

  sys_dev = json.loads(
  '''
    {
    "system_devices": {
      "core": [{
        "id": 0,
        "length":1.6,
        "fuel_channel_number": 1064,
        "channel_length_of_horizontal": "1.2*2.54/100",
        "channel_length_of_vertical": "0.2*2.54/100",
        "inside_diamiter":0.737,
        "heat_conductivity":150,
        "specific_heat": "0.4*4.2*2.2e6"
      }],
      "pump": [{
        "id": 1,
        "length":0.25,
        "vertical_length": "9.75*2.54/100",
        "horizontal_length": "13 * 2.54/100",
        "dia":"6 * 2.54 / 100 /1.4",
        "pump_volume": "5.75 * (0.305)**3",
        "impeller": "11.5 * 2.54/100",
        "inlet_x": 1.63,
        "inlet_y": 0,
        "inlet_z": 3.39,
        "outlet_x": 1.63,
        "outlet_y": 0,
        "outlet_z": 3.39,
        "heat_conductivity":94,
        "out_volume_persec_plus": 0.1,
        "out_volume_persec_minus": 1e-8,
        "specific_heat": "0.427*8.89e6",
        "thickness": "1*2.54/100"
      }],
      "heat_exchanger": [{
        "id": 2,
        "dia": 5e-3,
        "outside_diamiter": "1 * 2.54 / 100",
        "inside_diamiter": "0.8 * 2.54 / 100",
        "length":0.15,
        "length_of_utube": "173 * 2 / 100",
        "inlet_x": 3.30,
        "inlet_y": 0,
        "inlet_z": 3.39,
        "outlet_x": 3.30,
        "outlet_y": 0,
        "outlet_z": 3.39,
        "heat_conductivity":94,
        "utube_number": 156,
        "specific_heat": "0.427*8.89e6",
        "thickness": "0.1*2.54/100"
      }],
      "pipe": [
        {
          "id": 3,
          "dia": "6 * 2.54 / 100",
          "outside_diamiter": "8 * 2.54 / 100",
          "length":0.25,
          "inlet_x": 0,
          "inlet_y": 0,
          "inlet_z": 1.6,
          "outlet_x": 0,
          "outlet_y": 0,
          "outlet_z": 1.85,
          "heat_conductivity":94,
          "specific_heat": "0.427*8.89e6",
          "thickness": "1*2.54/100"
        },
        {
          "id": 4,
          "dia": "6 * 2.54 / 100",
          "outside_diamiter": "8 * 2.54 / 100",
          "length":0.25,
          "inlet_x": 0,
          "inlet_y": 0,
          "inlet_z": 1.6,
          "outlet_x": 0,
          "outlet_y": 0,
          "outlet_z": 1.85,
          "heat_conductivity":94,
          "specific_heat": "0.427*8.89e6",
          "thickness": "1*2.54/100"
        }]
      }
    }
  '''
  )['system_devices']
  return SystemManager(sys_cn, sys_dev, SystemEnv(sys_env))

def test_next_devices(sys_manager):
  assert 1 in [d.id for d in sys_manager.next_devices(0)]
  assert 3 in [d.id for d in sys_manager.next_devices(2)]
  assert 0 in [d.id for d in sys_manager.next_devices(4)]

def test_previous_devices(sys_manager):
  assert 0 in [d.id for d in sys_manager.previous_devices(1)]
  assert 2 in [d.id for d in sys_manager.previous_devices(3)]

def test_move_system(sys_manager):
  sys_manager_saved = sys_manager.copy()
  sys_manager.move_system(10, 1)
  for d in sys_manager.devices:
    d_bef = list(filter(lambda x: x.id == d.id, sys_manager_saved.devices))[0]
    d_bef_next = sys_manager_saved.next_devices(d_bef.id)[0]
    assert d.delta_volume_passing_boundary == 10
    assert d.velocity == d.delta_volume_passing_boundary / d.area_l_end_boundary / 1
    assert d.delta_mass_boundary == d.delta_volume_passing_boundary * d.density
    assert round(d.mass, 3) == round(d_bef.mass + d_bef.delta_mass_boundary - d_bef_next.delta_mass_boundary, 3)
