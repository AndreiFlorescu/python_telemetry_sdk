from dispatcher.Dispatcher import Dispatcher
from telemetry.Event import Event
import json


class ErrorEvent(Event):
    """
    The class of the ERROR event
    ...

    Attributes
    ----------
    request_info : Event
        The dictionary that will hold all the data of the event

    Methods
    -------
    set_event_data(message, status_code, err_type)
        Sets the data of the event
    __send_json()
        Send the data to the dispatcher
    """

    def __init__(self, message, status_code, err_type):
        self.request_info = Event()
        self.set_event_data(message, status_code, err_type)

    def set_event_data(self, message, status_code, err_type):
        edata = {
            'error': status_code,
            'errtype': err_type,
            'stacktrace': message
        }

        self.request_info.requestInfo['eid'] = 'ERROR'
        self.request_info.requestInfo['edata'] = edata
        self.__send_json()

    def __send_json(self):
        log_json = json.dumps(self.requestInfo)
        Dispatcher.add_telemetry_event(log_json, Event.lock)
