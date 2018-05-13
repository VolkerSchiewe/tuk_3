from consts import DB_TABLE


def trajectory_in_group_range_sample_point(trajectory_id, first_group_id, last_group_id):
    union_string = 'UNION ALL'
    filter_string = f'''
        WHERE FGID >= {first_group_id}
        AND FGID <= {last_group_id}
        AND TID = {trajectory_id}'''
    sql = f'''
            SELECT TID,
            FGID,
            Ix AS LON,
            Iy AS LAT
            FROM Taxi.{DB_TABLE}
            {filter_string}
            {union_string}
        '''

    for i in range(1, 119):
        sql += f'''
            SELECT TID,
            FGID,
            Ix + P{i}x AS LON,
            Iy + P{i}y AS LAT
            FROM Taxi.{DB_TABLE}
            {filter_string}
        '''
        sql += union_string if i < 118 else ''

    return sql


def trajectories_in_group_range(first_group_id, last_group_id, trajectory_id=None):
    sql = f'''
            SELECT TID,
            FGID,
            Ix,
            Iy,
        '''

    for i in range(1, 119):
        sql += f'''
            Ix + P{i}x AS P{i}x,
            Iy + P{i}y AS P{i}y
        '''
        sql += ',' if i != 118 else ''

    sql += f'''
        FROM Taxi.{DB_TABLE}
        WHERE FGID >= {first_group_id}
        AND FGID < {last_group_id}
    '''
    sql += f'AND TID = {trajectory_id}' if trajectory_id else ''

    return sql
