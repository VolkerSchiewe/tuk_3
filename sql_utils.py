from sql.create_table import get_create_table
from sql.frame_group import get_insert


def read_sql(file_name):
    with open(file_name) as f:
        return f.read()


def create_new_table(connection):
    connection.execute(get_create_table(120))


def insert_frame_groups(connection, frame_groups):
    for frame_group in frame_groups:
        sql = get_insert(frame_group)
        connection.execute(sql)
        print(f'Inserted frame group into db: {frame_group.trajectory_id}:{frame_group.frame_group_id}')
