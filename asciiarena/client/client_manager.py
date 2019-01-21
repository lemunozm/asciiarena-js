from common.package_queue import PackageQueue, InputPack, OutputPack
from common.logging import logger
from common import message

class ClientManager(PackageQueue):
    def __init__(self):
        PackageQueue.__init__(self)

    def init_communication(self, server):
        self._output_queue.put(OutputPack("First message", server))

