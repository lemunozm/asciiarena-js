from .package_queue import InputPack, OutputPack

import _pickle as pickle
import pynetstring

class PackageFactory:
    def __init__(self):
        self._decoder = pynetstring.Decoder()

    def create_input_packages(self, data, endpoint):
        input_pack_list = []
        message_data_list = self._decoder.feed(data)
        for message_data in message_data_list:
            message = pickle.loads(message_data)
            input_pack_list.append(InputPack(message, endpoint))

        return input_pack_list

    def process_output_package(self, output_package):
        data_endpoint_list = []
        message_data = pickle.dumps(output_package.message)
        data = pynetstring.encode(message_data)
        for endpoint in output_package.endpoint_list:
            data_endpoint_list.append((data, endpoint))

        return data_endpoint_list
