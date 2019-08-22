import os
import threading


class TelemetryConfig:

    """
    A class for configuring telemetry
    ...

    Attributes
    ----------
    lock : thread lock
        The lock used for locking threads
    telemetry_service_url : string
        The url of the telemetry server
    buffer_size : int
        The maximum number of events to be stored before sending
    buffer_time : int
        The time (in seconds) after which the telemetry package is sended automatically
    env : string
        The environment
    actor_type : string
        Type of actor
    actor_id : string
        Id of actor
    version : string
        Version used
    context : object of class Context
        Contains the basic information of telemetry events

    Methods
    -------
    get_context()
        Returns the context

    """

    lock = threading.Lock()
    telemetry_service_url = "http://10.67.120.27:9001/v1/telemetry"
    # telemetry_service_url = os.environ.get('TELEMETRY_SERVICE_URL')
    buffer_size = 3
    buffer_time = 2
    env = os.environ.get('ENV')
    actor_type = "Service"
    actor_id = os.environ.get('SERVICE_ID')
    version = "3.0"

    class Context:
        class PData:
            def __init__(self):
                return

            def get_id(self):
                return self.id

            def set_id(self, id):
                self.id = id

            def get_pid(self):
                return self.pid

            def set_pid(self, pid):
                self.pid = pid

            def get_version(self):
                return self.version

            def set_version(self, version):
                self.version = version

        def __init__(self):
            self.pData = self.PData()
            self.channel = ''

        def get_channel(self):
            return self.channel

        def set_channel(self, channel):
            self.channel = channel

        def get_p_data(self):
            return self.pData

    context = Context()

    def get_context(self):
        return self.context
