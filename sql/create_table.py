from consts import DB_TABLE


def get_create_table(frame_size):
    sql = f'''
        CREATE COLUMN TABLE {DB_TABLE} (
        TID INTEGER,
        FGID INTEGER,
        Ix DOUBLE,
        Iy DOUBLE,'''

    for i in range(1, frame_size):
        p_frame = f'''
        P{i}x DOUBLE,
        P{i}y DOUBLE'''

        last_frame = frame_size - 1

        if i < last_frame:
            p_frame += ','

        sql += p_frame

    sql += ')'
    return sql
