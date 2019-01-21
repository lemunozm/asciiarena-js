from common.package_queue import PackageQueue, InputPack, OutputPack
from common.logging import logger
from common import version, message

class ServerManager(PackageQueue):
    def __init__(self):
        PackageQueue.__init__(self)
        self._active = True

    def is_active(self):
        return self._active

    def process_package(self):
        input_pack = self._input_queue.get()
        version_message = input_pack.message

        validation = version.check(version_message.value)

        checked_version_message = message.CheckedVersion(version.CURRENT, validation)
        self._output_queue.put(OutputPack(checked_version_message, input_pack.endpoint))
