from record import Recorder, Record, InvalidUrlError, FileDoesNotExistError, IllegalRecordError
import pytest


def test_record_init():
    method, url = "PUT", "/a/b/c"
    record = Record("PUT", "/a/b/c", 10)
    assert isinstance(record, Record)
    assert record.response_time == 10
    assert record.method == method
    assert record.url == url
    assert record.key() == "{}^{}".format(url, method)


@pytest.mark.parametrize("test_input,expected", [
    ("/a/10/b", "/a/{id}/b"), ("/a/10", "/a/{id}"),
    ("/10/a/b", "/{id}/a/b")
])
def test_record_substitutes_digits(test_input, expected):
    record = Record("PUT", "/a/b/c/", 10)
    assert record._sanitize_url(test_input) == expected


def test_invalid_url_error():
    record = Record("PUT", "/a/b/c", 10)
    with pytest.raises(InvalidUrlError):
        record._sanitize_url("")


def test_recorder_creates_record_from_csv():
    recorder = Recorder("test_file")
    csv_row = ["132332", "/a/b/c", "PUT", 10]
    assert len(recorder._records) == 0
    recorder._create_record(csv_row)
    assert len(recorder._records) == 1


def test_recorder_raises_nofile_exception():
    recorder = Recorder("test_file")
    with pytest.raises(FileDoesNotExistError):
        recorder._read_csv()


def test_recorder_raises_illegal_record_error():
    recorder = Recorder("test_file")
    with pytest.raises(IllegalRecordError):
        csv_row = ["132332", "/a/b/c", "PUT1", 10]
        recorder._create_record(csv_row)
