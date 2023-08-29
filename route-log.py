from tools.lib.logreader import LogReader
from tools.lib.route import Route
from cereal import log as capnp_log

route = "../openpilot-routes/jprous-no-lkas.rlog.bz2"
lr = LogReader(route)

for log_msg in lr:
  msg_type = log_msg.which()
  if msg_type == 'can':
    print(log_msg.to_bytes())
