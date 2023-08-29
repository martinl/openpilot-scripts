#! python3
from tools.lib.logreader import LogReader
from tools.lib.route import Route
import codecs

# capnproto <= 0.8.0 throws errors converting byte data to string
# below line catches those errors and replaces the bytes with \x__
codecs.register_error("strict", codecs.backslashreplace_errors)

# Frye - Outback 2021
#route_id = '36e19891049b91e3|2021-06-28--16-26-11'

# ursubpar - Outback 2020 PCB alert issue when filtering LKAS
#route_id = '7393c1b180278950|2021-06-29--13-00-40'

# Crispin - Crosstrek 2020 
#route_id='8bf7e79a3ce64055|2021-05-24--09-36-27'

# martinl - Crosstrek 2018
#ROUTE=05bca04dfbdca165\|2021-07-01--21-54-54

# Rabid - Levorg 2016
#ROUTE=133acd9637109da2\|2021-07-03--20-34-37

# cfarra - WRX vehicle parameter error
#route_id = 'd345d482f9119a3f|2021-07-22--08-59-18'

# SSM4
route_id='05bca04dfbdca165|2021-11-09--14-01-37'

route = Route(route_id)
log_paths = route.log_paths()
#events_seg0 = list(LogReader(log_paths[0]))
#print(len(events_seg0), 'events logged in first segment')

for log_path in log_paths:
  #print(log_path)
  lr = LogReader(log_path)

  for log_msg in lr:
    msg_type = log_msg.which()
    #print(msg_type)
    if msg_type == 'can':
      for rec in log_msg.can:
        print("%s;%s;%s;%s" % (log_msg.logMonoTime, rec.src, rec.address, rec.dat.hex()))
    #if msg_type == 'initData':
      #print(log_msg)
