MAX_BUFFER_SIZE = 4096

class Version:
    def __init__(self, value):
        self.value = value

class CheckedVersion:
    def __init__(self, value, validation):
        self.value = value
        self.validation = validation
