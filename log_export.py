from tools.lib.logreader import LogReader
from tools.lib.route import Route
from cereal import log as capnp_log
from collections import defaultdict
import cantools
import sys

route_id = sys.argv[1]
dbc_file = 'opendbc/subaru_crosstrek_2018.dbc'
#route = Route(route_id)

# bus, addr, msg, signal
signals = [
  (  0,  64, "Throttle", "Engine_RPM"),
  (  0,  64, "Throttle", "Throttle_Cruise"),
  (  0,  73, "CVT", "CVT_Gear"),
  (  0, 576, "CruiseControl", "Cruise_Activated"),
  (128, 544, "ES_Brake", "Brake_Pressure"),
  (128, 545, "ES_Distance", "Cruise_Throttle"),
  (128, 546, "ES_Status", "Cruise_RPM"),
]

keys = ['Engine_RPM', 'Throttle_Cruise', 'Cruise_Activated', 'Cruise_Throttle', 'Cruise_RPM', 'Brake_Pressure', 'v_ego', 'a_ego', 'v_cruise', 'computer_gas', 'computer_brake', 'a_target', 'v_target']

dbc = cantools.database.load_file(dbc_file)
table = defaultdict(dict)
can_msg = defaultdict(dict)
prev_logMonoTime = 0 

for i in signals:
  msg = i[2]
  can_msg[msg] = dbc.get_message_by_name(msg)

#log_paths = route.log_paths()

comma = ","
print('logMonoTime,' + comma.join(keys))

#for log_path in log_paths:
  #print(log_path)
lr = LogReader(log_path)

for log_msg in lr:
  msg_type = log_msg.which()
  #print(msg_type)
  if msg_type == 'can':
    for rec in log_msg.can:
      for s in signals:
        bus, addr, msg, signal = list(s)
        if (bus == rec.src and addr == rec.address):
          table[log_msg.logMonoTime][signal] = can_msg[msg].decode(rec.dat)[signal]
          #print("%s: %s" % (signal, can_msg[msg].decode(rec.dat)[signal]))
          #print("%s %s %s %s %s:%s" % (log_msg.logMonoTime, msg_type, rec.src, rec.address, signal, can_sig))
  elif msg_type == 'carState':
    table[log_msg.logMonoTime]['v_ego'] = log_msg.carState.vEgo
    table[log_msg.logMonoTime]['a_ego'] = log_msg.carState.aEgo
    table[log_msg.logMonoTime]['v_cruise'] = log_msg.carState.cruiseState.speed
    #print("%s %s %s %s %s" % (log_msg.logMonoTime, msg_type, log_msg.carState.vEgo, log_msg.carState.aEgo, log_msg.carState.cruiseState.speed))
  elif msg_type == 'carControl':
      table[log_msg.logMonoTime]['computer_gas'] = log_msg.carControl.actuators.gas
      table[log_msg.logMonoTime]['computer_brake'] = log_msg.carControl.actuators.brake
      #print("%s %s %s %s" % (log_msg.logMonoTime, msg_type, log_msg.carControl.actuators.gas, log_msg.carControl.actuators.brake))
    elif msg_type == 'plan':
      table[log_msg.logMonoTime]['a_target'] = log_msg.plan.aTarget
      table[log_msg.logMonoTime]['v_target'] = log_msg.plan.vTarget
      #print("%s %s %s %s" % (log_msg.logMonoTime, msg_type, log_msg.plan.aTarget, log_msg.plan.vTarget))

    if prev_logMonoTime != log_msg.logMonoTime and len(table) > 0 :
      for time, items in table.items():
        result = str(time)
        for k in keys:
          #print(items[k])
          try:
            result += "," + str(items[k])
          except KeyError:
            result += ","
        print(result)
      table = defaultdict(dict)

    prev_logMonoTime = log_msg.logMonoTime

'''
    plot_arr[:-1] = plot_arr[1:]
    plot_arr[-1, name_to_arr_idx['angle_steers']] = sm['controlsState'].angleSteers
    plot_arr[-1, name_to_arr_idx['angle_steers_des']] = sm['carControl'].actuators.steerAngle
    plot_arr[-1, name_to_arr_idx['angle_steers_k']] = angle_steers_k
    plot_arr[-1, name_to_arr_idx['gas']] = sm['carState'].gas
    plot_arr[-1, name_to_arr_idx['computer_gas']] = sm['carControl'].actuators.gas
    plot_arr[-1, name_to_arr_idx['user_brake']] = sm['carState'].brake
    plot_arr[-1, name_to_arr_idx['steer_torque']] = sm['carControl'].actuators.steer * ANGLE_SCALE
    plot_arr[-1, name_to_arr_idx['computer_brake']] = sm['carControl'].actuators.brake
    plot_arr[-1, name_to_arr_idx['v_ego']] = sm['controlsState'].vEgo
    plot_arr[-1, name_to_arr_idx['v_pid']] = sm['controlsState'].vPid
    plot_arr[-1, name_to_arr_idx['v_override']] = sm['carControl'].cruiseControl.speedOverride
    plot_arr[-1, name_to_arr_idx['v_cruise']] = sm['carState'].cruiseState.speed
    plot_arr[-1, name_to_arr_idx['a_ego']] = sm['carState'].aEgo
    plot_arr[-1, name_to_arr_idx['a_target']] = sm['plan'].aTarget
    plot_arr[-1, name_to_arr_idx['accel_override']] = sm['carControl'].cruiseControl.accelOverride
'''
