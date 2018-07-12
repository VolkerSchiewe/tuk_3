from sql.create_table import get_create_table
from sql.frame_group import get_insert
from sql.create_key_value import get_create_key_value_table, get_drop_key_value_table
from sql.key_value import get_insert_key_value, get_insert_key_values_nclob, get_insert_key_value_trips, \
    get_insert_key_values_trips_nclob
from consts import NCLOB_MAX_COMMIT, DB_TABLE_KEY_VALUE


def read_sql(file_name):
    with open(file_name) as f:
        return f.read()


def create_new_table(connection):
    connection.execute(get_create_table(30))


def create_key_value_format(connection):
    connection.execute(get_drop_key_value_table())
    connection.execute(get_create_key_value_table())


def insert_key_value(connection, key_value):
    sql = get_insert_key_value(key_value)
    connection.execute(sql)
    print(key_value.obj)
    print(len(key_value.obj))
    for i in range(int(len(key_value.obj) / NCLOB_MAX_COMMIT) + 1):
        nclob_data = key_value.obj[i * NCLOB_MAX_COMMIT:(i + 1) * NCLOB_MAX_COMMIT - 1]
        update = get_insert_key_values_nclob(key_value.id, nclob_data)
        connection.execute(update)
    print(f'Inserted key-value pair into db: {key_value.id}:{key_value.mbr}')


def insert_key_value_trips(connection, key_trips):
    if len(key_trips.obj) < NCLOB_MAX_COMMIT:
        sql = get_insert_key_value_trips(key_trips)
        connection.execute(sql)
    else:
        nclob = key_trips.obj
        key_trips.obj = ''
        sql = get_insert_key_value_trips(key_trips)
        connection.execute(sql)
        chunks = [nclob[i: i + NCLOB_MAX_COMMIT] for i in range(0, len(nclob), NCLOB_MAX_COMMIT)]

        for chunk in chunks:
            update = get_insert_key_values_trips_nclob(key_trips.id, chunk)
            connection.execute(update)

    print(f'Inserted key-value pair into db: (id) {key_trips.id}: (start t in sec) {key_trips.start}: (end t in sec) {key_trips.end}: (mbr) {key_trips.mbr}')
    print(f'Sample size: {len(key_trips.obj)}')


def insert_frame_groups(connection, frame_groups):
    for frame_group in frame_groups:
        sql = get_insert(frame_group)
        connection.execute(sql)
        print(f'Inserted frame group into db: {frame_group.trajectory_id}:{frame_group.frame_group_id}')
