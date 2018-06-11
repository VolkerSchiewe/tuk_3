import csv

from point_trip.trip_utils import add_trip_ids
from utils.hana_connector import HanaConnection


def create_trip_format(connection):
    connection.execute('SELECT DISTINCT ID FROM POINT')
    trajectory_ids = connection.fetchall()

    for trajectory_id, in trajectory_ids:
        connection.execute(f'SELECT * FROM POINT WHERE ID = {trajectory_id} ORDER BY HOUR, MINUTE, SECOND')
        points = connection.fetchall()
        converted_points = add_trip_ids(points)
        _save_to_csv(converted_points, 'point_trips.csv')


def create_table(connection):
    connection.execute('DROP TABLE POINT_TRIPS')
    connection.execute('''CREATE COLUMN TABLE POINT_TRIPS (
            TRAJECTORY_ID INTEGER,
            TRIP_ID INTEGER,
            HOUR INTEGER,
            MINUTE INTEGER,
            SECOND INTEGER,
            LON DOUBLE,
            LAT DOUBLE,
            OCCUPANCY INTEGER,
            SPEED INTEGER)''')


def _save_to_csv(points, file):
    with open(file, 'a') as f:
        writer = csv.writer(f)
        writer.writerows(points)
    print('Inserted', points[0][0])


if __name__ == '__main__':
    with HanaConnection('TUK3_HNKS') as c:
        # create_table(c)
        create_trip_format(c)
