from .package_queue import InputPack, OutputPack

import _pickle as pickle
import pynetstring
import threading

class PackageFactory:
    def __init__(self):
        self._decoder_dict = {}
        self._mutex = threading.Lock()

    def create_input_packages(self, data, endpoint):
        with self._mutex:
            decoder = self._decoder_dict.get(endpoint, pynetstring.Decoder())

            input_pack_list = []
            message_data_list = decoder.feed(data)
            for message_data in message_data_list:
                message = pickle.loads(message_data)
                input_pack_list.append(InputPack(message, endpoint))

            return input_pack_list

    def process_output_package(self, output_package):
        data_endpoint_list = []
        message_data = pickle.dumps(output_package.message)
        data = pynetstring.encode(message_data)
        return data, output_package.endpoint_list

    def untrack_endpoint(self, endpoint):
        with self._mutex:
            if self._decoder_dict.get(endpoint, None):
                del self._decoder_dict[endpoint]

