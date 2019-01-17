import _pickle as pickle
import queue
import threading

class Request:
    def __init__(self, sender, request_message):
        self.sender = sender
        self.request_message = request_message

class Reply:
    def __init__(self, receiver_list, reply_message):
        self.receiver_list = receiver_list
        self.reply_message = reply_message

class ProcessingError(Error):
    pass

class Processor:
    def __init__(self, game_manager):
        self._request_queue = queue.Queue()
        self._reply_queue = queue.Queue()
        self._running = False

    @abstractmethod
    def process_request(self, request):
        pass

    def run(self):
        self._running = True
        thread = threading.Thread(target = self._request_processing)
        thread.start()

    def stop():
        self._running = False

    def is_running():
        return self._running

    def queue_request(self, request):
        self._request_queue.put(request)

    def dequeue_reply(self):
        return self._reply_queue.get()

    def _request_processing(self):
        while self._running:
            request = self._request_queue.get()
            reply = self.process_request(request)
            self._reply_queue.put(reply)

