from config.TelemetryConfig import TelemetryConfig
import uuid
from datetime import datetime


class Event:
    """
    The class that handles the basic information of the telemetry events
    ...

    Attributes
    ----------
    telemetry_config : class
        The object that holds all the information regarding the configuration of the telemetry
    messageId : str
        The message ID (mid) of the event
    requestInfo : dict
        The dictionary that will hold all the data of the event
    lock : thread lock
        The lock used for threads
    """

    telemetry_config = TelemetryConfig()

    messageId = ""
    requestInfo = {}
    lock = TelemetryConfig.lock

    def __init__(self):

        if not self.messageId.strip():
            self.messageId = str(uuid.uuid4())

        self.requestInfo['eid'] = ''
        self.requestInfo['ets'] = int(datetime.timestamp(datetime.now()) * 1000)
        self.requestInfo['ver'] = self.telemetry_config.version
        self.requestInfo['mid'] = self.messageId

        self.requestInfo['actor'] = {'id': self.telemetry_config.actor_id, 'type': self.telemetry_config.actor_type}

        req_context = {}

        channel = self.telemetry_config.get_context().get_channel()

        req_context['channel'] = channel
        req_context['env'] = self.telemetry_config.env

        self.requestInfo['context'] = req_context
