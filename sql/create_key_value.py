from consts import DB_TABLE_KEY_VALUE


def get_drop_key_value_table():
    return f'DROP TABLE {DB_TABLE_KEY_VALUE}'


def get_create_key_value_table():
    return f'''
    CREATE COLUMN TABLE {DB_TABLE_KEY_VALUE} (
        id INTEGER,
        obj NCLOB,
        st INTEGER,
        et INTEGER,
        mbr VARCHAR(50)
    )'''
