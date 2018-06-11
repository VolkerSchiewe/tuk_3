from consts import DB_TABLE
from frame_trip.models.frame_group import FrameGroup


def get_insert(frame_group: FrameGroup):
    x = '0' if frame_group.i_frame.x is None else frame_group.i_frame.x
    y = '0' if frame_group.i_frame.y is None else frame_group.i_frame.y

    sql = f'''
        INSERT INTO {DB_TABLE} VALUES (
        {frame_group.trajectory_id},
        {frame_group.frame_group_id},
        {frame_group.trip_id},
        {frame_group.occupancy},
        {x},
        {y},'''

    for i, frame in enumerate(frame_group.p_frames):
        x = 'NULL' if frame.x is None else frame.x
        y = 'NULL' if frame.y is None else frame.y

        p_frame = f'''{x},
                      {y}'''

        last_frame = len(frame_group.p_frames) - 1

        if i < last_frame:
            p_frame += ','

        sql += p_frame

    sql += ')'
    return sql
