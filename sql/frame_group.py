from consts import DB_TABLE


def get_insert(frame_group):
    sql = f'''
        INSERT INTO {DB_TABLE} VALUES (
        {frame_group.trajectory_id},
        {frame_group.frame_group_id},
        {frame_group.trajectory_id},
        {frame_group.i_frame.x},
        {frame_group.i_frame.y},'''

    for i, frame in enumerate(frame_group.p_frames):
        p_frame = f'''{frame.x},
                      {frame.y}'''

        last_frame = len(frame_group.p_frames) - 1

        if i < last_frame:
            p_frame += ','

        sql += p_frame

    sql += ')'
    return sql
