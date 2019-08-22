import time
from datetime import datetime
from telemetry.AuditEvent import AuditEvent
from telemetry.ErrorEvent import ErrorEvent
from telemetry.LogEvent import LogEvent
from dispatcher.Dispatcher import Dispatcher

Dispatcher()
ErrorEvent('test', 'test', 'test')
LogEvent('test', 'test', 'test', {'ha': 'haha'})
time.sleep(2)
# print(int(datetime.timestamp(datetime.now()) * 1000))
ErrorEvent('test', '', '')
AuditEvent('test', '', '')
LogEvent('test', '', '')
