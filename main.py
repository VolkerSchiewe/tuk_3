from frame_utils import interpolate_missing_frames, group_frames, delta_encode, add_padding
from hana_connector import HanaConnection
from models.frame_group import FrameGroup
from models.sample import Sample
from models.key_value import KeyValue
from sample_utils import sample_with_highest_sed
from sql.get_trajectories_shark import trajectories_in_group_range
from sql_utils import read_sql, insert_frame_groups, create_new_table, insert_key_value, create_key_value_format, insert_key_value_trips
from tracker import Tracker
import os
import json

tracker = Tracker()


def run():
    with HanaConnection() as connection:
        # IF SCHEMA = 'TUK3_HNKS'
        connection.execute("SELECT DISTINCT ID FROM POINT_TRIPS ORDER BY ID;")

        # connection.execute(read_sql("./sql/trajectories.sql"))
        trajectories = connection.fetchall()
        # create_new_table(connection)
        create_key_value_format(connection)

        for trajectory_id in trajectories:
            # if SCHEMA = 'TUK3_HNKS'
            connection.execute("SELECT * FROM POINT_TRIPS WHERE ID = {} ORDER BY TIMESTAMP".format(trajectory_id[0]))
            trajectory = connection.fetchall()
            key_trips = create_key_trips(trajectory_id[0], trajectory)
            insert_key_value_trips(connection, key_trips)
            # write_row_to_file(key_trips)
            print(f'Trajectory for trip {trajectory_id[0]} was processed')

            # connection.execute(read_sql("./sql/get_trajectory.sql").format(trajectory_id[0]))
            # trajectory = connection.fetchall()
            # key_value = create_key_value(trajectory_id[0], trajectory)
            # insert_key_value(connection, key_value)
            # print(f'Trajectory {trajectory_id} was processed')

            #frames = create_frames(trajectory)
            #frame_groups = create_frame_groups(trajectory_id[0], frames)
            #insert_frame_groups(connection, frame_groups)
            #tracker.print()


def write_to_csv(key_value: KeyValue):
    download_dir = "key_trips.csv"  # where you want the file to be downloaded to

    csv = open(download_dir, "w")
    row = f'''{key_value.id}, {key_value.obj}, {key_value.start}, {key_value.end}, {key_value.mbr}'''
    csv.write(row)


def write_row_to_file(key_value: KeyValue):
    row = [str(key_value.id), str(key_value.obj), str(key_value.start), str(key_value.end), str(key_value.mbr)]
    joined = ";".join(row)
    with open('key_value.csv', 'a') as file:
        file.write(joined)
        file.write(os.linesep)


def create_key_trips(trajectory_id, trajectory):
    trajectory_obj = []
    x = []
    y = []
    for row in trajectory:
        sample = Sample.from_point_trips_row(row)
        timestamp = sample.timestamp
        trajectory_obj.append([timestamp, sample.x, sample.y])
        x.append(sample.x)
        y.append(sample.y)

    trajectory_object = json.dumps(trajectory_obj)
    sample_st = Sample.from_point_trips_row(trajectory[0])
    trajectory_st = sample_st.timestamp

    # get trajectory end timestamp
    sample_et = Sample.from_point_trips_row(trajectory[-1])
    trajectory_et = sample_et.timestamp
    trajectory_mbr = [min(x), min(y), max(x), max(y)]
    key_trips = KeyValue(trajectory_id, trajectory_object, trajectory_st, trajectory_et, trajectory_mbr)
    return key_trips


def create_key_value(trajectory_id, trajectory):

    # creating trajectory object
    trajectory_obj = []
    x = []
    y = []
    for row in trajectory:
        sample = Sample.from_row(row)
        timestamp = str(sample.timestamp)
        trajectory_obj.append([timestamp, sample.x, sample.y])
        x.append(sample.x)
        y.append(sample.y)

    trajectory_object = json.dumps(trajectory_obj)
    print(trajectory_object)

    # get trajectory start timestamp
    sample_st = Sample.from_row(trajectory[0])
    trajectory_st = sample_st.timestamp

    # get trajectory end timestamp
    sample_et = Sample.from_row(trajectory[-1])
    trajectory_et = sample_et.timestamp

    # MBR: A rectangle, oriented to the x- and y-axes,
    # that bounds a geographic feature or a geographic dataset.
    # It is specified by two coordinate pairs: xmin, ymin and xmax, ymax.
    trajectory_mbr = [min(x), min(y), max(x), max(y)]
    key_value = KeyValue(trajectory_id, trajectory_object, trajectory_st, trajectory_et, trajectory_mbr)
    return key_value


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
    groups = group_frames(frames, 30)
    frame_groups = []

    for (group_id, trip_id, occupancy), frames in groups.items():
        padded_frames = add_padding(frames, 30)
        i_frame = None
        p_frames = []
        if len(padded_frames) > 0:
            i_frame = padded_frames[0]
        if len(padded_frames) > 1:
            p_frames = [delta_encode(i_frame, frame) for frame in padded_frames[1:len(padded_frames)]]

        frame_groups.append(FrameGroup(trajectory_id, group_id, trip_id, occupancy, i_frame, p_frames))

    return frame_groups


def run_requests(begin_frame, begin_end, trajectory_id=None):
    with HanaConnection() as connection:
        connection.execute(trajectories_in_group_range(begin_frame, begin_end, trajectory_id))
        return connection.fetchall()


if __name__ == '__main__':
    # run_requests(0, 1)
    run()
