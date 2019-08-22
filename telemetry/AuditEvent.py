from telemetry.Event import Event
from dispatcher.Dispatcher import Dispatcher
import json


class AuditEvent(Event):
    """
    The class of the AUDIT event
    ...

    Attributes
    ----------
    request_info : Event
        The dictionary that will hold all the data of the event

    Methods
    -------
    set_event_data(state, argv)
        Sets the data of the event
    __send_json()
        Send the data to the dispatcher
    """

    def __init__(self, state, *argv):
        self.request_info = Event()
        self.set_event_data(state, argv)

    def set_event_data(self, state, argv):
        edata = {
            'props': state
        }

        if len(argv) is 2:
            edata['state'] = argv[0]
            edata['prevstate'] = argv[1]

        self.request_info.requestInfo['eid'] = 'AUDIT'
        self.request_info.requestInfo['edata'] = edata
        self.__send_json()

    def __send_json(self):
        log_json = json.dumps(self.requestInfo)
        Dispatcher.add_telemetry_event(log_json, Event.lock)
