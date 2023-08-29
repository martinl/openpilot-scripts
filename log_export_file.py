#
# usage: python log_export_file.py file.rlog2 > file.csv
#
from tools.lib.logreader import LogReader
from tools.lib.route import Route
from cereal import log as capnp_log
from collections import defaultdict
import cantools
import sys

log_path = sys.argv[1]
dbc_file = 'opendbc/subaru_global_2017_generated.dbc'

# bus, addr, msg, signal
signals = [
  (  0, 281, "Steering_Torque", "Steering_Angle"),
  (  0, 281, "Steering_Torque", "Steer_Torque_Sensor"),
  (  0, 281, "Steering_Torque", "Steer_Torque_Output"),
  (  0, 576, "CruiseControl", "Cruise_Activated"),
  (128, 290, "ES_LKAS", "LKAS_Output"),
  (128, 290, "ES_LKAS", "LKAS_Request"),
]

keys = ['Steering_Angle', 'Steer_Torque_Sensor', 'Steer_Torque_Output', 'Cruise_Activated', 'LKAS_Output', 'LKAS_Request', 'v_ego', 'a_ego', 'v_cruise']

dbc = cantools.database.load_file(dbc_file)
table = defaultdict(dict)
can_msg = defaultdict(dict)
prev_logMonoTime = 0 

for i in signals:
  msg = i[2]
  can_msg[msg] = dbc.get_message_by_name(msg)

comma = ","
print('logMonoTime,' + comma.join(keys))

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
          #print("%s %s %s %s %s:%s" % (log_msg.logMonoTime, msg_type, rec.src, rec.address, signal, can_msg[msg].decode(rec.dat)[signal]))
  elif msg_type == 'carState':
    table[log_msg.logMonoTime]['v_ego'] = log_msg.carState.vEgo
    table[log_msg.logMonoTime]['a_ego'] = log_msg.carState.aEgo
    table[log_msg.logMonoTime]['v_cruise'] = log_msg.carState.cruiseState.speed
    #print("%s %s %s %s %s" % (log_msg.logMonoTime, msg_type, log_msg.carState.vEgo, log_msg.carState.aEgo, log_msg.carState.cruiseState.speed))

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
