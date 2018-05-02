import numpy as np

from hana_connector import HanaConnection
from models.frame import Frame
from models.frame_group import FrameGroup
from sql.create_table import get_create_table
from sql.frame_group import get_insert
from utils import read_sql


def run():
    with HanaConnection() as connection:
        connection.execute(read_sql("./sql/trajectories.sql"))
        trajectories = connection.fetchall()
        # create_new_table(connection)

        for trajectory_id in trajectories:
            frames = []
            connection.execute(read_sql("./sql/get_trajectory.sql").format(trajectory_id[0]))
            trajectory = connection.fetchall()
            for sample in trajectory:
                frame_id = sample[1].hour * 60 + sample[1].minute
                frame = Frame(frame_id, sample[2], sample[3])

                if len(frames) > 0 and frame_id == frames[-1].id:
                    # todo SED
                    continue
                if len(frames) > 0 and frame_id != frames[-1].id + 1:
                    interpolated_frames = interpolate(frames[-1], frame)
                    frames = frames + interpolated_frames
                frames.append(frame)

            frame_groups = create_frame_groups(trajectory_id[0], frames)
            insert_frame_groups(connection, frame_groups)


def interpolate(previous, following):
    x = range(previous.id + 1, following.id)
    array_lon = np.interp(x, (previous.id, following.id), (previous.x, following.x))
    array_lat = np.interp(x, (previous.id, following.id), (previous.y, following.y))
    array = []
    for i in range(len(array_lon)):
        array.append(Frame(x[i], array_lon[i], array_lat[i]))
    return array


def create_frame_groups(trajectory_id, frames):
    groups = group_frames_by_hour(frames)
    frame_groups = []

    for group_id, frames in groups.items():
        i_frame = None
        p_frames = []

        if len(frames) > 0:
            i_frame = frames[0]
        if len(frames) > 1:
            p_frames = [delta_encode(i_frame, frame) for frame in frames[1:len(frames)]]
        # TODO: Remove padding!
        if len(p_frames) < 60:
            for i in range(len(p_frames) + 1, 60):
                p_frames.append(Frame(0, 0, 0))
        frame_groups.append(FrameGroup(trajectory_id, group_id, i_frame, p_frames))

    return frame_groups


def group_frames_by_hour(frames):
    grouped_frames = {}

    for frame in frames:
        group_id = int(frame.id / 60) + 1
        if group_id not in grouped_frames:
            grouped_frames[group_id] = list()
        grouped_frames[group_id].append(frame)

    return grouped_frames


def delta_encode(i_frame, frame):
    x = i_frame.x - frame.x
    y = i_frame.y - frame.y
    return Frame(frame.id, x, y)


def create_new_table(connection):
    connection.execute(get_create_table(60))


def insert_frame_groups(connection, frame_groups):
    for frame_group in frame_groups:
        sql = get_insert(frame_group)
        connection.execute(sql)
        print(f'Inserted frame group into db: {frame_group.trajectory_id}:{frame_group.frame_group_id}')

def run_requests():
    with HanaConnection() as connection:
        connection.execute(get_time_frame(1, 2, top_k=1000))
        return connection.fetchall()

if __name__ == '__main__':
    run()
