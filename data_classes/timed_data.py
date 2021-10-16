import json
from datetime import datetime
import time 

class TimedData:
  def __init__(self, data, timestamp = time.mktime(datetime.now().timetuple())):
    self.data = data
    self.timestamp = timestamp