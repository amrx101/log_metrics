class FileDoesNotExistError(Exception):
    def __init__(self, msg):
        self.message = msg


class NoDataRowError(Exception):
    def __init__(self):
        self.message = "No data row in the given csv file"


class InvalidUrlError(Exception):
    def __init__(self, url):
        self.message = "URL={} is invalid".format(url)


class IllegalRecordError(Exception):
    def __init__(self, msg):
        self.message = msg
