from app import logic
from app import models


_statistics = logic.Statistics()


def server_arranged_durations():
    return _statistics.server_arranged_durations()


def add_report(report: models.Report):
    _statistics.increase_counts(report)


def report_available(durations_by_servers):
    return _statistics.report_available(durations_by_servers)


def mean(durations_by_servers):
    return _statistics.mean(durations_by_servers)


def deviation(durations_by_servers):
    return _statistics.deviation(durations_by_servers)


def outlier_server_names(durations_by_servers):
    return _statistics.outlier_server_names(durations_by_servers)
