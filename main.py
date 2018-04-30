from hana_connector import HanaConnection
from utils import read_sql


def create_frame_groups():
    with HanaConnection() as connection:
        # todo change sql script
        connection.execute(read_sql("./sql/trajectories.sql"))
        trajectories = connection.fetchall()

        for trajectory in trajectories:
            print(trajectory)


def interpolate():
    pass


def create_new_table():
    pass


def push_data():
    pass
