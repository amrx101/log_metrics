class NoFreqRecordError(Exception):
    def __init__(self):
        self.message = "Empty frequency distribution table created from CSV file"


class NoTimingRecordsError(Exception):
    def __init__(self):
        self.message = "Empty timing table created from csv file"
