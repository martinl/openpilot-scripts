#!/usr/local/bin/python3
import csv
import cantools
import binascii
from collections import defaultdict

'''
- 0:64 Throttle Throttle_Cruise
- 0:64 Throttle Engine_RPM
- 0:72 Transmission RPM
- 0:576 CruiseControl Cruise_Activated
- 128:545 ES_Distance Cruise_Throttle
- 128:546 ES_Status Cruise_RPM
'''

dbc_file = 'opendbc/subaru_crosstrek_2018.dbc'
csv_file = 'subaru_crosstrek_2018-op-long-2000-highway-1586901005093.csv'

# signals to extract from cabana csv
signals = defaultdict(dict)
signals[0]['bus'] = 0
signals[0]['addr'] = 64
signals[0]['msg'] = 'Throttle'
signals[0]['signal'] = 'Throttle_Cruise'

signals[1]['bus'] = 0
signals[1]['addr'] = 64
signals[1]['msg'] = 'Throttle'
signals[1]['signal'] = 'Engine_RPM'

signals[2]['bus'] = 0
signals[2]['addr'] = 72
signals[2]['msg'] = 'Transmission'
signals[2]['signal'] = 'RPM'

signals[3]['bus'] = 128
signals[3]['addr'] = 545
signals[3]['msg'] = 'ES_Distance'
signals[3]['signal'] = 'Cruise_Throttle'

signals[4]['bus'] = 128
signals[4]['addr'] = 546
signals[4]['msg'] = 'ES_Status'
signals[4]['signal'] = 'Cruise_RPM'

signals[5]['bus'] = 0
signals[5]['addr'] = 576
signals[5]['msg'] = 'CruiseControl'
signals[5]['signal'] = 'Cruise_Activated'

dbc = cantools.database.load_file(dbc_file)
table = defaultdict(dict)
can_msg = defaultdict(dict)

for i in signals:
  msg = signals[i]['msg']
  can_msg[msg] = dbc.get_message_by_name(msg)

with open(csv_file, newline = '') as csvfile:
  reader = csv.DictReader(csvfile)
  for row in reader:
    time = row['time']
    data = binascii.unhexlify(row['data'])
    for i in signals:
      bus = str(signals[i]['bus'])
      addr = str(signals[i]['addr'])
      msg = signals[i]['msg']
      signal = signals[i]['signal']

      if (row['bus'] == bus and row['addr'] == addr):
        table[time][signal] = can_msg[msg].decode(data)[signal]

header = "time"
for i in signals:
  signal = signals[i]['signal']
  header += "," + signal
print(header)

for time, items in table.items():
  result = time
  for i in signals:
    signal = signals[i]['signal']
    try:
      result += ',' + str(items[signal])
    except KeyError:
      result += ','
  print(result)
