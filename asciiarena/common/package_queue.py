import queue

class InputPack:
    def __init__(self, message, endpoint):
        self.message = message
        self.endpoint = endpoint

class OutputPack:
    def __init__(self, message, endpoint):
        if isinstance(endpoint, list):
            self.endpoint_list = endpoint
        else:
            self.endpoint_list = [endpoint]
        self.message = message

class PackageQueue():
    def __init__(self):
        self._input_queue = queue.Queue()
        self._output_queue = queue.Queue()

    def enqueue_input(self, package):
        self._input_queue.put(package)

    def dequeue_output(self, timeout = 0):
        try:
            return self._output_queue.get(True, timeout)
        except queue.Empty:
            return None

