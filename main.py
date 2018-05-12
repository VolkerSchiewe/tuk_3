from frame_utils import interpolate_missing_frames, group_frames_by_hour, delta_encode, add_padding
from hana_connector import HanaConnection
from models.frame_group import FrameGroup
from models.sample import Sample
from sample_utils import sample_with_highest_sed
from sql_utils import read_sql, create_new_table, insert_frame_groups
from tracker import Tracker

tracker = Tracker()


def run():
    with HanaConnection() as connection:
        connection.execute(read_sql("./sql/trajectories.sql"))
        trajectories = connection.fetchall()
        # create_new_table(connection)

        for trajectory_id in trajectories:
            connection.execute(read_sql("./sql/get_trajectory.sql").format(trajectory_id[0]))
            trajectory = connection.fetchall()
            frames = create_frames(trajectory)
            frame_groups = create_frame_groups(trajectory_id[0], frames)
            insert_frame_groups(connection, frame_groups)
            tracker.print()


def create_frames(trajectory):
    frames = []
    current_frame_id = 0
    samples_in_frame = []

    for row in trajectory:
        tracker.track_sample()
        sample = Sample.from_row(row)
        in_current_frame = sample.frame_id() == current_frame_id

        if not in_current_frame:
            if len(samples_in_frame) > 0:
                # Create a frame from collected samples, uses SED if necessary
                previous_frame = frames[-1] if len(frames) > 0 else samples_in_frame[0].to_frame()
                following_frame = sample.to_frame()
                selected_sample = sample_with_highest_sed(samples_in_frame, previous_frame, following_frame)
                frames.append(selected_sample.to_frame())
                tracker.track_frame(len(samples_in_frame))
                samples_in_frame = []

            # Interpolate missing frames
            if len(frames) > 0 and sample.frame_id() != current_frame_id + 1:
                interpolated_frames = interpolate_missing_frames(frames[-1], sample.to_frame())
                tracker.track_interpolated_frames(len(interpolated_frames))
                frames = frames + interpolated_frames
            current_frame_id = sample.frame_id()

        samples_in_frame.append(sample)

    # Flush pending samples
    if len(samples_in_frame) > 0:
        previous_frame = frames[-1] if len(frames) > 0 else samples_in_frame[0].to_frame()
        following_frame = samples_in_frame[-1].to_frame()
        selected_sample = sample_with_highest_sed(samples_in_frame, previous_frame, following_frame)
        frames.append(selected_sample.to_frame())
    return frames


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
        padded_p_frames = add_padding(p_frames, 119)
        frame_groups.append(FrameGroup(trajectory_id, group_id, i_frame, padded_p_frames))

    return frame_groups

def run_requests():
    with HanaConnection() as connection:
        connection.execute(get_time_frame(1, 2, top_k=1000))
        return connection.fetchall()


if __name__ == '__main__':
    run()
