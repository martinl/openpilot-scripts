import os
import re
import pycurl
import urllib
import argparse
from tools.lib.route import Route

parser = argparse.ArgumentParser(description='openpilot route to download')
parser.add_argument('route', nargs='?')
args = parser.parse_args()

if args.route is None:
  print("no route is provided")
  exit(1)

r = Route(args.route)

'''
# get a list of paths for the route's rlog files
print("rlog")
print(r.log_paths())
print("qcamera")
print(r.qcamera_paths())
print("ecamera")
print(r.ecamera_paths())
print("camera")
print(r.camera_paths())
'''

rlog_urls = r.log_paths()
qlog_urls = r.qlog_paths()
fcamera_urls = r.camera_paths()
qcamera_urls = r.qcamera_paths()
ecamera_urls = r.ecamera_paths()

for urls in [rlog_urls, qlog_urls, fcamera_urls, qcamera_urls, ecamera_urls]:
  for url in urls:
    if url is not None:
      #print(url)
      url_path = urllib.parse.urlparse(url).path
      file = re.sub("(\/preserve\/|\/qlog\/|\/commadata2\/)", "route/", url_path)
      path = os.path.dirname(file)
      print(path)
      os.makedirs(path, exist_ok = True)
      print("Downloading: %s" % file)
      with open(file, 'wb') as f:
        c = pycurl.Curl()
        c.reset()
        c.setopt(pycurl.FOLLOWLOCATION, True)
        c.setopt(pycurl.URL, url)
        c.setopt(c.WRITEDATA, f)
        c.perform()
        c.close()
      f.close()
