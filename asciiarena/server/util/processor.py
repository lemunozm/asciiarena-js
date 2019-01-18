import queue
import threading
import _pickle as pickle

class Request:
    def __init__(self, sender, message):
        self.sender = sender
        self.message = message

class Reply:
    def __init__(self, receiver_list, message):
        self.receiver_list = receiver_list
        self.message = message

class ProcessingError(Exception):
    pass

class Processor(object):
    def __init__(self):
        self._request_queue = queue.Queue()
        self._reply_queue = queue.Queue()
        self._running = False

    #abstractmethod
    def process_request(self, request):
        pass

    def run(self):
        self._running = True
        thread = threading.Thread(target = self._request_processing)
        thread.start()

    def stop(self):
        self._running = False
        self._request_queue.put(None)

    def is_running(self):
        return self._running

    def enqueue_request(self, request):
        self._request_queue.put(request)

    def dequeue_reply(self):
        return self._reply_queue.get()

    def _request_processing(self):
        while self._running:
            request = self._request_queue.get()
            reply = self.process_request(request) if None != request else None
            self._reply_queue.put(reply)

