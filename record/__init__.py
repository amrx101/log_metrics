import csv
import logging
import os
import sys
import urlparse
from collections import defaultdict
from error import FileDoesNotExistError, NoDataRowError, InvalidUrlError, IllegalRecordError


logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
log = logging.getLogger(__name__)

consoleHandler = logging.StreamHandler(sys.stdout)
consoleHandler.setFormatter(logFormatter)
log.addHandler(consoleHandler)
log.setLevel("DEBUG")


class Record(object):
    def __init__(self, method, url, response_time):
        self._method = method
        self._url = self._sanitize_url(url)
        self._response_time = response_time

    def _sanitize_url(self, url):
        parsed = urlparse.urlparse(url)
        path = parsed.path
        if path:
            components = path.split("/")
            components = ["{id}" if _comp.isdigit() else _comp for _comp in components]
            return "/".join(components)
        raise InvalidUrlError(url)

    @property
    def method(self):
        return self._method

    @property
    def url(self):
        return self._url

    @property
    def response_time(self):
        return self._response_time

    def key(self):
        return "{}^{}".format(self.url, self.method)


class Recorder(object):
    def __init__(self, file_name):
        self.file_name = file_name
        self._methods = set()
        self._methods.add("PUT")
        self._methods.add("GET")
        self._methods.add("POST")
        self._records = defaultdict(lambda: [0, 0, float("-inf"), float("inf")])

    def start(self):
        log.debug("Starting Recorder to capture log file.")
        self._read_csv()
        log.debug("Successfully started Recorder.")

    def _read_csv(self):
        if os.path.exists(self.file_name) and os.path.getsize(self.file_name) > 0:
            log.debug("Reading log file={}".format(self.file_name))
            l_cnt = 0
            with open(self.file_name) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=",")
                for row in csv_reader:
                    if l_cnt == 0:
                        l_cnt += 1
                        continue
                    self._create_record(row)
                    l_cnt += 1
            if l_cnt < 2:
                log.error("Only header in the csv file. Records missing")
                raise NoDataRowError()
        else:
            raise FileDoesNotExistError("File={} either does not exists or is empty".format(self.file_name))

    def _create_record(self, csv_row):
        url, method, response_time = csv_row[1], csv_row[2], csv_row[3]
        if method not in self._methods:
            raise IllegalRecordError("Invalid method={} in record.".format(method))
        try:
            record = Record(method, url, response_time)
            key = record.key()
            response_time = int(response_time)
            self._records[key][0] += 1
            self._records[key][1] += response_time
            self._records[key][2] = max(self._records[key][2], response_time)
            self._records[key][3] = min(self._records[key][3], response_time)

        except InvalidUrlError as e:
            log.error(e.message)

    def generate_reports(self):
        records = sorted(self._records.items(), key=lambda i: i[1], reverse=True)
        freq_table = []
        timing_table = []
        for key, value in records:
            url, method = key.split("^")
            freq, _sum, _max, _min = value[0], float(value[1]), value[2], value[3]
            avg = _sum / freq
            freq_rec = [method, url, freq]
            timing_rec = [method, url, _min, _max, avg]
            freq_table.append(freq_rec)
            timing_table.append(timing_rec)
        return freq_table, timing_table
