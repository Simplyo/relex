import json

import flask
import werkzeug.exceptions

from app import db
from app import decoders
from app import statistics

app = flask.Flask(__name__)


@app.route('/process_report', methods=['POST'])
def process_report():
    content = flask.request.json
    report = decoders.decoded_report(content)
    statistics.add_report(report)
    response = app.make_response('')
    return response


@app.route('/process_statistics', methods=['GET'])
def process_statistics():
    durations = statistics.server_arranged_durations()
    if not statistics.report_available(durations):
        return error_response()

    mean = statistics.mean(durations)
    deviation = statistics.deviation(durations)
    return flask.jsonify(
        mean=mean,
        stddev=deviation,
    )


@app.route('/process_outliers', methods=['GET'])
def process_outliers():
    durations = statistics.server_arranged_durations()
    if not statistics.report_available(durations):
        return error_response()

    outlier_server_names = statistics.outlier_server_names(durations)
    return flask.jsonify(outlier_server_names)


def error_response():
    error = werkzeug.exceptions.InternalServerError()
    response = error.get_response()
    response.data = json.dumps({
        'error': 'Not enough reports received',
    })
    response.content_type = "application/json"
    return response


@app.teardown_appcontext
def close_connection(exception):
    db.close_connection(exception)


if __name__ == '__main__':
    app.run()
