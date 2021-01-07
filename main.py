import argparse
import logging
import sys

from record import Recorder
from report import Reporter

logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
log = logging.getLogger(__name__)


consoleHandler = logging.StreamHandler(sys.stdout)
consoleHandler.setFormatter(logFormatter)
log.addHandler(consoleHandler)
log.setLevel("DEBUG")


class Application(object):
    def __init__(self, file_name):
        self._file_name = file_name
        self._recorder = Recorder(self._file_name)
        self._reporter = Reporter(self._recorder)

    def start(self):
        self.start_services()
        self.print_report()

    def _make_app(self):
        pass

    def start_services(self):
        self._recorder.start()

    def print_report(self):
        self._reporter.display_report()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', help="location of log file", dest="file", type=str)
    args = parser.parse_args()
    app = Application(args.file)
    app.start()

