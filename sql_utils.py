from sql.create_table import get_create_table
from sql.frame_group import get_insert
from sql.create_key_value import get_create_key_value_table
from sql.key_value import get_insert_key_value, get_insert_key_values_nclob
from consts import NCLOB_MAX_COMMIT
from consts import DB_TABLE_KEY_VALUE


def read_sql(file_name):
    with open(file_name) as f:
        return f.read()


def create_new_table(connection):
    connection.execute(get_create_table(30))


def create_key_value_format(connection):
    connection.execute(get_create_key_value_table())


def insert_key_value(connection, key_value):
    sql = get_insert_key_value(key_value)
    connection.execute(sql)
    print(len(key_value.obj))
    print(NCLOB_MAX_COMMIT)
    for i in range(int(len(key_value.obj) / NCLOB_MAX_COMMIT) + 1):
        nclob_data = key_value.obj[i * NCLOB_MAX_COMMIT:(i + 1) * NCLOB_MAX_COMMIT - 1]
        update = get_insert_key_values_nclob(key_value.id, str(nclob_data))
        # update = f'''UPDATE {DB_TABLE_KEY_VALUE} SET TRAJECTORY_OBJECT='{nclob_data}' WHERE TRAJECTORY_ID={key_value.id}'''
        connection.execute(update)
    print(f'Inserted key-value pair into db: {key_value.id}:{key_value.mbr}')


def insert_frame_groups(connection, frame_groups):
    for frame_group in frame_groups:
        sql = get_insert(frame_group)
        connection.execute(sql)
        print(f'Inserted frame group into db: {frame_group.trajectory_id}:{frame_group.frame_group_id}')
