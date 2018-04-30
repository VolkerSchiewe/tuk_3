from hana_connector import HanaConnection
from models.frame import Frame
from utils import read_sql
import numpy as np


def create_frame_groups():
    with HanaConnection() as connection:
        connection.execute(read_sql("./sql/trajectories.sql"))
        trajectories = connection.fetchall()

        for trajectory_id in trajectories:
            frames = []
            connection.execute(read_sql("./sql/get_trajectory.sql").format(trajectory_id[0]))
            trajectory = connection.fetchall()
            for sample in trajectory:
                frame_id = sample[1].hour * 60 + sample[1].minute
                frame = Frame(frame_id, sample[2], sample[3])

                if len(frames) > 0 and frame_id == frames[-1].id:
                    # todo SED
                    pass
                if len(frames) > 0 and frame_id != frames[-1].id + 1:
                    interpolated_frames = interpolate(frames[-1], frame)
                    frames = frames + interpolated_frames
                frames.append(frame)

            # todo create framegroups
            # todo save frame group in hana
            pass


def interpolate(previous, following):
    x = range(previous.id, following.id)  # todo find point between previous and following
    array = np.interp(x, previous, following)
    # todo create ew frames
    return array


def create_new_table():
    pass


def push_data():
    pass


if __name__ == '__main__':
    create_frame_groups()
