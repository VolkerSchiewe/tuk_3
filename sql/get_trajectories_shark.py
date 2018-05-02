from consts import DB_TABLE


def get_trajs_in_frame(fgid, fid, top_k=None):
    top_string = ''
    if top_k:
        top_string = f'''TOP {top_k}'''

    sql = f'''
    SELECT {top_string} TID,
    Ix + P{fid}x as LON,
    Iy + P{fid}y as LAT
    FROM {DB_TABLE}
    WHERE FGID = {fgid}
    '''
    return sql

def get_trajs_in_frame_range(first_fgid, last_fgid, first_fid, last_fid, top_k=None):
    # TODO change column names when column names were renamed
    top_string = ''
    if top_k:
        top_string = f'''TOP {top_k}'''

    sql = ''
    filter_string = f'''WHERE FGID >= {first_fgid} AND FGID <= {last_fgid}'''
    union_string = 'UNION ALL'

    for i in range(first_fid, last_fid + 1):
        sql += f'''
        SELECT {top_string} TID,
        Ix + P{i}x as LON,
        Iy + P{i}y as LAT
        FROM {DB_TABLE}
        {filter_string} 
        '''
        if i != last_fid:
            sql += union_string

    return sql
