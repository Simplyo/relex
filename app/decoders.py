import datetime

from app import models

DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'


def decoded_report(json_content):
    start = datetime.datetime.strptime(json_content['start_time'], DATETIME_FORMAT)
    end = datetime.datetime.strptime(json_content['end_time'], DATETIME_FORMAT)
    duration = int((end - start).total_seconds())
    return models.Report(
        server_name=json_content['server_name'],
        duration=duration,
    )
