from consts import DB_TABLE

def get_time_frame(frame_group_id, frame_id, top_k=None):
    # TODO change when column names were renamed
    if top_k == None:
        top_string = ''
    else:
        top_string = f'''TOP {top_k}'''
    sql = f'''
    SELECT {top_string} FGID,
    Ix + P{frame_id}x as LON,
    Iy + P{frame_id}y as LAT
    FROM {DB_TABLE}
    WHERE TID = {frame_group_id}
    '''
    return sql
