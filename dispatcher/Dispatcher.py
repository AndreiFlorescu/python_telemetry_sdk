from config.TelemetryConfig import TelemetryConfig
import time
from datetime import datetime
import threading
import requests


class Dispatcher:
    """
    A class for sending the telemetry events
    ...

    Attributes
    ----------
    queue : list
        The list that contains the jsons
    current_pos : int
        The number of jsons in the queue
    buffer_size : int
        The maximum number of events to be sent at once
    buffer_time : int
        The maximum time (in seconds) before a buffer is sent
    locked : bool
        Used for waiting for the queue to be cleared before adding more events to it

    Methods
    -------
    every(delay, task, lock)
        Makes sure that telemetry is sended if a certain amount of time passes
    add_telemetry_event(request_info, lock)
        Adds an event to the list of events
    __send_data(lock)
        Sends data to where it is supposed to
    __data_to_server()
        Sends data to server
    """

    queue = []
    current_pos = 0
    buffer_size = 0
    buffer_time = 0
    locked = False

    def __init__(self):
        Dispatcher.buffer_size = TelemetryConfig.buffer_size
        Dispatcher.buffer_time = TelemetryConfig.buffer_time

        self.lock = TelemetryConfig.lock
        threading.Thread(target=lambda: Dispatcher.every(Dispatcher.buffer_time, Dispatcher.__send_data, self.lock)).start()

    @staticmethod
    def every(delay, task, lock):
        next_time = time.time() + delay

        while True:
            time.sleep(max(0, next_time - time.time()))
            task(lock)
            next_time += (time.time() - next_time) // delay * delay + delay

    @staticmethod
    def add_telemetry_event(request_info, lock):
        print(str(datetime.timestamp(datetime.now()) * 1000))
        while Dispatcher.locked is True:
            pass
        Dispatcher.queue.append(request_info)
        Dispatcher.current_pos += 1
        # time.sleep(0.00001)

        if Dispatcher.current_pos is Dispatcher.buffer_size:
            # send data to server
            Dispatcher.__send_data(lock)

    @staticmethod
    def __send_data(lock):

        Dispatcher.locked = True
        lock.acquire()
        print(str(datetime.timestamp(datetime.now()) * 1000) + f' {threading.current_thread()}')
        if Dispatcher.current_pos is not 0:
            Dispatcher.__data_to_server()

        Dispatcher.queue = []
        Dispatcher.current_pos = 0
        lock.release()
        Dispatcher.locked = False

    @staticmethod
    def __data_to_server():
        data = {
            'telemetry': Dispatcher.queue
        }

        try:
            r = requests.post(url=TelemetryConfig.telemetry_service_url, data=data)
        except (Exception, ) as e:
            print("Something went wrong: " + f"{e}")
