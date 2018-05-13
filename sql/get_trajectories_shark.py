from consts import DB_TABLE
from models.frame import Frame


def get_trajs_in_frame(group_id, frame_id, top_k=None):
    top_k_str = f'TOP {top_k}' if top_k else ''
    lon_str = 'Ix' if frame_id == 0 else f'Ix + P{frame_id}x'
    lat_str = 'Iy' if frame_id == 0 else f'Iy + P{frame_id}y'

    sql = f'''
    SELECT {top_k_str} TID,
    {lon_str} as LON,
    {lat_str} as LAT
    FROM {DB_TABLE}
    WHERE FGID = {group_id}
    '''
    return sql


def get_trajectories_in_range(connection, first_group_id, first_frame_id, last_group_id, last_frame_id, top_k=None):
    top_k_str = f'TOP {top_k}' if top_k else ''
    connection.execute(f'''
        SELECT {top_k_str} *
        FROM {DB_TABLE}
        WHERE FGID >= {first_group_id} AND FGID <= {last_group_id}
        ORDER BY TID, FGID
    ''')

    frame_groups = connection.fetchall()
    frames = []

    for frame_group in frame_groups:
        begin = first_frame_id if frame_group[1] == first_group_id else 0
        end = last_frame_id if frame_group[1] == last_group_id else 119

        for frame_id in range(begin, end):
            frames.append(delta_decode_frame(frame_group, frame_id))

    return frames


def delta_decode_frame(frame_group, frame_id):
    assert 0 <= frame_id <= 119
    # TODO: Convert to format that is better for visualisation, e.g. timestamp.
    original_frame_id = frame_group[1] * frame_id
    index = frame_id * 2
    frame = Frame(original_frame_id, frame_group[index], frame_group[index + 1])

    if frame_id == 0:
        return frame
    else:
        i_frame = delta_decode_frame(frame_group, 0)
        return Frame(original_frame_id, i_frame.x + frame.x, i_frame.y + frame.y)
