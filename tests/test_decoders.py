import app.decoders
import app.models


class TestDecodeReport:

    def test_decoded_report(self):
        json_content = {
            'server_name': 't-0945532345',
            'start_time': '2021-05-17T10:12:33Z',
            'end_time': '2021-05-17T23:50:19Z',
        }
        report = app.decoders.decoded_report(json_content)
        assert isinstance(report, app.models.Report)
        assert report.duration == 49066.0
        assert report.server_name == 't-0945532345'
