import queue

class PackageQueue():
    def __init__(self):
        self._input_queue = queue.Queue()
        self._output_queue = queue.Queue()

    def enqueue_input(self, package):
        self._input_queue.put(package)

    def dequeue_output(self):
        return self._output_queue.get()

