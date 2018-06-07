from sql.create_table import get_create_table
from sql.frame_group import get_insert
from sql.create_key_value import get_create_key_value_table
from sql.key_value import get_insert_key_value


def read_sql(file_name):
    with open(file_name) as f:
        return f.read()


def create_new_table(connection):
    connection.execute(get_create_table(30))


def create_key_value_format(connection):
    connection.execute(get_create_key_value_table())


def insert_key_value(connection, key_value):
    sql = get_insert_key_value(key_value)
    print(sql)
    connection.execute(sql)
    print(f'Inserted key-value pair into db: {key_value.id}:{key_value.mbr}')


def insert_frame_groups(connection, frame_groups):
    for frame_group in frame_groups:
        sql = get_insert(frame_group)
        connection.execute(sql)
        print(f'Inserted frame group into db: {frame_group.trajectory_id}:{frame_group.frame_group_id}')
