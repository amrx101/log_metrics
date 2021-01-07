import logging
import sys

from tabulate import tabulate
from error import NoFreqRecordError, NoTimingRecordsError

logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
log = logging.getLogger(__name__)

consoleHandler = logging.StreamHandler(sys.stdout)
consoleHandler.setFormatter(logFormatter)
log.addHandler(consoleHandler)
log.setLevel("DEBUG")


class Reporter(object):
    def __init__(self, recorder):
        self._recorder = recorder
        self._freq_headers = ["METHOD", "URL", "FREQUENCY"]
        self._timing_headers = ["METHOD", "URL", "Min Time", "Max Time", "Average Time"]
        self._style = "github"

    def _print_report(self, table, headers):
        print tabulate(table, headers, tablefmt=self._style)

    def display_report(self):
        freq_table, timing_table = self._recorder.generate_reports()
        self._print_report(freq_table, self._freq_headers)
        print "\n"
        print "\n"
        self._print_report(timing_table, self._timing_headers)