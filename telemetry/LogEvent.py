from dispatcher.Dispatcher import Dispatcher
from telemetry.Event import Event
import json


class LogEvent(Event):
    """
    The class of the LOG event
    ...

    Attributes
    ----------
    request_info : Event
        The dictionary that will hold all the data of the event

    Methods
    -------
    set_event_data(type, level, message, argv)
        Sets the data of the event
    __send_json()
        Send the data to the dispatcher
    """

    def __init__(self, type, level, message, *argv):
        self.request_info = Event()
        self.set_event_data(type, level, message, argv)

    def set_event_data(self, type, level, message, argv):
        edata = {
            'type': type,
            'level': level,
            'message': message
        }

        if len(argv) is 1:
            edata['params'] = argv[0]

        self.request_info.requestInfo['eid'] = 'LOG'
        self.request_info.requestInfo['edata'] = edata
        self.__send_json()

    def __send_json(self):
        log_json = json.dumps(self.requestInfo)
        Dispatcher.add_telemetry_event(log_json, Event.lock)
