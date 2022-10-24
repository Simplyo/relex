import math
import typing

from app import db
from app import models

TOTAL_REPORTS_REQUIRED_THRESHOLD = 10
SERVER_REPORTS_REQUIRED_THRESHOLD = 3


class Statistics:

    @staticmethod
    def increase_counts(report: models.Report) -> None:
        db.server_duration_save(
            server_name=report.server_name,
            duration=report.duration,
        )

    @staticmethod
    def server_arranged_durations():
        servers_durations = db.servers_durations()
        durations = models.Durations()

        for server_name, duration in servers_durations:
            durations.add(server_name, duration)

        return durations

    @staticmethod
    def report_available(durations: models.Durations) -> bool:
        counter = len(durations.durations())
        if counter < TOTAL_REPORTS_REQUIRED_THRESHOLD:
            return False

        minimal_reports_per_server = min(
            len(durations) for durations in durations.server_durations()
        )

        if minimal_reports_per_server < SERVER_REPORTS_REQUIRED_THRESHOLD:
            return False

        return True

    @staticmethod
    def mean(durations: models.Durations, server_name: str = None) -> int:
        server_durations = durations.durations(server_name)
        duration_sum = sum(server_durations)
        return round(duration_sum/len(server_durations))

    def _deviation(self, durations: models.Durations, mean: int, server_name: str = None) -> int:
        squares_sum = 0
        server_durations = durations.durations(server_name)
        for duration in server_durations:
            diff_with_average = duration - mean
            squares_sum += diff_with_average * diff_with_average
        deviation = round(
            math.sqrt(squares_sum/(len(server_durations) - 1))
        )
        return deviation

    def deviation(self, durations: models.Durations) -> int:
        mean = self.mean(durations)
        deviation = self._deviation(durations, mean)
        return deviation

    def _deviation_range(self, durations: models.Durations, server_name: str) -> typing.Tuple[int, int]:
        mean = self.mean(durations, server_name)
        deviation = self._deviation(durations, mean, server_name)
        three_deviations = 3 * deviation
        deviation_range = (
            mean - three_deviations,
            mean + three_deviations,
        )
        return deviation_range

    @staticmethod
    def _outlier(durations: models.Durations, min_duration: int, max_duration: int, server_name: str = None) -> bool:
        for duration in durations.durations(server_name):
            if duration < min_duration:
                return True

            if max_duration < duration:
                return True

        return False

    def outlier_server_names(self, durations: models.Durations) -> typing.List[str]:
        server_names = set()
        for server_name in durations.server_names():
            min_duration, max_duration = self._deviation_range(durations, server_name)
            if self._outlier(durations, min_duration, max_duration, server_name):
                server_names.add(server_name)
        return sorted(server_names)
