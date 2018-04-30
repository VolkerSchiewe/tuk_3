from hana_connector import HanaConnection
from utils import read_sql
import numpy as np


def create_frame_groups():
    with HanaConnection() as connection:
        # todo change sql script
        connection.execute(read_sql("./sql/trajectories.sql"))
        trajectories = connection.fetchall()

        for trajectory in trajectories:
            # todo get trajectory
            # todo interpolate
            # todo create framegroups
            # todo save frame group in hana
            pass


def interpolate(previous, following):
    np.interp()
    pass


def create_new_table():
    pass


def push_data():
    pass
