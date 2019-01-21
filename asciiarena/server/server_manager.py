from common.package_queue import PackageQueue
from common.logging import logger
from common import message

class ServerManager(PackageQueue):
    def __init__(self):
        PackageQueue.__init__(self)

    def process_package(self):
        input_pack = self._input_queue.get()
        self._output_queue.put(InputPack(input_pack.message, input_pack.endpoint))
