import typing

from app import logic
from app import models


_statistics = logic.Statistics()


def server_arranged_durations():
    return _statistics.server_arranged_durations()


def add_report(report: models.Report):
    _statistics.increase_counts(report)


def report_available(durations: models.Durations):
    return _statistics.report_available(durations)


def mean(durations: models.Durations):
    return _statistics.mean(durations)


def deviation(durations: models.Durations):
    return _statistics.deviation(durations)


def outlier_server_names(durations: models.Durations):
    return _statistics.outlier_server_names(durations)
