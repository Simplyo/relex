import os
import sqlite3

import flask

DATABASE_FILE_NAME = 'relex.db'


def get_db():
    db = getattr(flask.g, '_database', None)
    db_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', 'sql', DATABASE_FILE_NAME)
    )
    if db is None:
        db = flask.g._database = sqlite3.connect(db_path)
    return db


def close_connection(exception):
    db = getattr(flask.g, '_database', None)
    if db is not None:
        db.close()


def server_duration_save(server_name, duration):
    connection = get_db()
    cursor = connection.cursor()
    query = "insert into durations (name, duration) values ('{name}', {duration});".format(
        name=server_name,
        duration=duration,
    )
    cursor.execute(query)
    connection.commit()


def servers_durations():
    connection = get_db()
    cursor = connection.cursor()
    query = "select name, duration from durations;"
    cursor.execute(query)
    return cursor.fetchall()
