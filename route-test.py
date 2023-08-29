from tools.lib.logreader import LogReader
import codecs

# capnproto <= 0.8.0 throws errors converting byte data to string
# below line catches those errors and replaces the bytes with \x__
codecs.register_error("strict", codecs.backslashreplace_errors)

route = "../openpilot-api/d345d482f9119a3f/2021-07-02--16-31-11/0/qlog.bz2"
lr = LogReader(route)

for log_msg in lr:
  msg_type = log_msg.which()
  #print(msg_type)
  if msg_type == 'carParams':
    print(log_msg)
