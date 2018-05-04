from frame_utils import interpolate_missing_frames
from hana_connector import HanaConnection
from models.frame import Frame
from models.frame_group import FrameGroup
from models.sample import Sample
from sample_utils import sample_with_highest_sed
from sql.create_table import get_create_table
from sql.frame_group import get_insert
from sql_utils import read_sql


def run():
    with HanaConnection() as connection:
        connection.execute(read_sql("./sql/trajectories.sql"))
        trajectories = connection.fetchall()
        # create_new_table(connection)

        for trajectory_id in trajectories:
            connection.execute(read_sql("./sql/get_trajectory.sql").format(trajectory_id[0]))
            trajectory = connection.fetchall()
            frame_groups = create_frame_groups_for_trajectory(trajectory_id[0], trajectory)
            insert_frame_groups(connection, frame_groups)


def create_frame_groups_for_trajectory(trajectory_id, trajectory):
    frames = []
    current_frame_id = 0
    samples_in_frame = []

    for row in trajectory:
        sample = Sample.from_tuple(row)
        is_first = len(frames) == 0
        in_current_frame = sample.frame_id() == current_frame_id()

        if is_first or in_current_frame:
            samples_in_frame.append(sample)
            current_frame_id = sample.frame_id()
        else:
            # New sample is not in the same frame, create new frame from previous samples
            # When only a single sample was collected, it is returned, otherwise sed is used.
            selected_sample = sample_with_highest_sed(samples_in_frame, frames[-1], sample.to_frame())
            frames.append(selected_sample.to_frame())

            # See if additional frames have to be generated
            expected_frame_id = frames[-1].id + 1

            if sample.frame_id() != expected_frame_id:
                interpolated_frames = interpolate_missing_frames(frames[-1], sample.to_frame())
                frames = frames + interpolated_frames

    return create_frame_groups(trajectory_id, frames)


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


if __name__ == '__main__':
    run()
