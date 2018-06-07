from consts import DB_TABLE_KEY_VALUE


def get_create_key_value_table():
    sql = f'''
        CREATE COLUMN TABLE {DB_TABLE_KEY_VALUE} (
        trajectory_id INTEGER,
        trajectory_object NCLOB,
        trajectory_st TIMESTAMP,
        trajectory_et TIMESTAMP,
        trajectory_mbr VARCHAR(255)'''

    sql += ')'
    return sql
