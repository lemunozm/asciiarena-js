from common.package_queue import PackageQueue, InputPack, OutputPack
import queue

MESSAGE_TIMEOUT = 5

class MessageTimeoutError(Exception):
    def __init__(self, timeout):
        self.timeout = timeout

class MessageQueue(PackageQueue):

    def __init__(self):
        PackageQueue.__init__(self)

    def _attach_endpoint(self, endpoint):
        self._endpoint = endpoint

    def _receive_message(self):
        return self._input_queue.get().message

    def _receive_message_timeout(self):
        try:
            return self._input_queue.get(timeout = MESSAGE_TIMEOUT).message
        except queue.Empty:
            raise MessageTimeoutError(MESSAGE_TIMEOUT)

    def _send_message(self, message):
        self._output_queue.put(OutputPack(message, self._endpoint))

    def _end_communication(self):
        self._output_queue.put(OutputPack(None, self._endpoint))

