from consts import DB_TABLE_KEY_VALUE
from models.key_value import KeyValue


def get_insert_key_value(key_value: KeyValue):
    sql = f'''
        INSERT INTO {DB_TABLE_KEY_VALUE} VALUES (
        {key_value.id},
        {key_value.obj},
        {key_value.start},
        {key_value.end},
        {key_value.mbr}'''

    sql += ')'
    return sql
