import os.path
import sqlite3

import pytest
import werkzeug.wrappers.response

import app.db
import app.logic
import app.models
import app.run
import app.statistics

TEST_DATABASE_FILE_NAME = 'relex_test.db'


@pytest.fixture()
def mock_jsonify(monkeypatch):
    def _jsonify(*args, **kwargs):
        return *args, kwargs

    monkeypatch.setattr('app.run.flask.jsonify', _jsonify)


class TestProcessReport:

    @pytest.fixture()
    def mock_request(self, monkeypatch):
        class _Request:
            json = {
                'server_name': 'Server name',
                'start_time': '2021-05-17T10:12:33Z',
                'end_time': '2021-05-17T23:57:19Z',
            }
        monkeypatch.setattr('app.run.flask.request', _Request)

    def test_process_report(self, mock_request, mocker):
        mock_add_report = mocker.patch('app.statistics.add_report')
        response = app.run.process_report()
        assert mock_add_report.call_args.args == (
            app.models.Report(
                server_name='Server name',
                duration=49486.0,
            ),
        )
        assert isinstance(response, werkzeug.wrappers.response.Response)
        assert response.status_code == 200
        assert response.data == b''
        assert response.mimetype == 'text/html'


def _add_reports(server_name, number, duration=None):
    report = app.models.Report(
        server_name=server_name,
        duration=duration or 9.0,
    )
    for index in range(number):
        app.run.statistics.add_report(report)


@pytest.fixture()
def mock_get_db(monkeypatch):
    def _get_db():
        db_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', 'sql', TEST_DATABASE_FILE_NAME)
        )
        return sqlite3.connect(db_path)
    monkeypatch.setattr('app.db.get_db', _get_db)


@pytest.fixture
def mock_statistics(mock_get_db):
    yield
    db_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', 'sql', TEST_DATABASE_FILE_NAME)
    )
    con = sqlite3.connect(db_path)
    cursor = con.cursor()
    query = "delete from durations;"
    cursor.execute(query)
    con.commit()


@pytest.mark.usefixtures('mock_statistics')
class TestProcessStatistics:

    def test_process_statistics(self, mock_jsonify):
        _add_reports(server_name='Name A', number=10)
        response = app.run.process_statistics()
        assert response == ({'mean': 9, 'stddev': 0}, )

    def test_process_statistics_total_reports_required_threshold(self):
        _add_reports(server_name='Name A', number=9)
        response = app.run.process_statistics()
        assert isinstance(response, werkzeug.wrappers.response.Response)
        assert response.status_code == 500
        assert response.data == b'{"error": "Not enough reports received"}'
        assert response.mimetype == 'application/json'

    def test_process_statistics_server_reports_required_threshold(self):
        _add_reports(server_name='Name A', number=10)
        _add_reports(server_name='Name B', number=2)
        response = app.run.process_statistics()
        assert isinstance(response, werkzeug.wrappers.response.Response)
        assert response.status_code == 500
        assert response.data == b'{"error": "Not enough reports received"}'
        assert response.mimetype == 'application/json'


@pytest.mark.usefixtures('mock_statistics')
class TestProcessOutliers:

    def test_process_outliers(self, mock_jsonify):
        _add_reports(server_name='Name A', number=10)
        _add_reports(server_name='Name A', number=1, duration=37.0)
        response = app.run.process_outliers()
        assert response == (['Name A'], {})

    def test_process_outliers_total_reports_required_threshold(self):
        _add_reports(server_name='Name A', number=9)
        response = app.run.process_outliers()
        assert isinstance(response, werkzeug.wrappers.response.Response)
        assert response.status_code == 500
        assert response.data == b'{"error": "Not enough reports received"}'
        assert response.mimetype == 'application/json'

    def test_process_outliers_server_reports_required_threshold(self):
        _add_reports(server_name='Name A', number=10)
        _add_reports(server_name='Name B', number=2)
        response = app.run.process_outliers()
        assert isinstance(response, werkzeug.wrappers.response.Response)
        assert response.status_code == 500
        assert response.data == b'{"error": "Not enough reports received"}'
        assert response.mimetype == 'application/json'


class TestErrorResponse:

    def test_error_response(self):
        response = app.run.error_response()
        assert isinstance(response, werkzeug.wrappers.response.Response)
        assert response.status_code == 500
        assert response.data == b'{"error": "Not enough reports received"}'
        assert response.mimetype == 'application/json'
