from common.package_queue import PackageQueue, InputPack, OutputPack
from common.logging import logger
from common import version, message

class ClientManager(PackageQueue):
    def __init__(self):
        PackageQueue.__init__(self)

    def init_communication(self, server):
        version_message = message.Version(version.CURRENT)
        self._output_queue.put(OutputPack(version_message, server))

        input_pack = self._input_queue.get()
        checked_version_message = input_pack.message

        compatibility = "COMPATIBLE" if checked_version_message.validation else "INCOMPATIBLE"
        print("Client version: {} - server version: {} - {}".format(version.CURRENT, checked_version_message.value, compatibility))
        print("")

