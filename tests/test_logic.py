import app.logic
import app.models


class TestStatistics:

    def mock_durations(self, number=None):
        durations = app.models.Durations()
        for index, (server_name, duration) in enumerate([
            ('Name A', 23),
            ('Name A', 23),
            ('Name A', 24),
            ('Name B', 23),
            ('Name A', 21),
            ('Name A', 24),
            ('Name A', 27),
            ('Name A', 27),
            ('Name A', 23),
            ('Name A', 23),
            ('Name A', 23),
            ('Name C', 32),
            ('Name A', 360),
            ('Name C', 300),
            ('Name B', 23),
            ('Name B', 23),
            ('Name C', 33),
            ('Name C', 33),
        ]):
            if number is not None and index >= number:
                return durations

            durations.add(server_name, duration)
        return durations

    def test_report_not_available_total_threshold(self, ):
        statistics = app.logic.Statistics()
        durations = self.mock_durations(number=9)
        assert statistics.report_available(durations) is False

    def test_report_not_available_server_threshold(self):
        statistics = app.logic.Statistics()
        durations = self.mock_durations(number=15)
        assert statistics.report_available(durations) is False

    def test_report_available(self):
        statistics = app.logic.Statistics()
        durations = self.mock_durations()
        assert statistics.report_available(durations) is True

    def test_mean(self):
        statistics = app.logic.Statistics()
        durations = self.mock_durations()
        assert statistics.mean(durations) == 59

    def test_deviation(self):
        statistics = app.logic.Statistics()
        durations = self.mock_durations()
        assert statistics.deviation(durations) == 99

    def test_outlier_server_names(self):
        statistics = app.logic.Statistics()
        durations = self.mock_durations()
        assert statistics.outlier_server_names(durations) == ['Name A']
