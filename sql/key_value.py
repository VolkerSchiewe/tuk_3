from consts import DB_TABLE_KEY_VALUE
from consts import NCLOB_MAX_COMMIT
from models.key_value import KeyValue


def get_insert_key_value(key_value: KeyValue):
    sql = f'''
        INSERT INTO {DB_TABLE_KEY_VALUE} (
        TRAJECTORY_ID, 
        TRAJECTORY_OBJECT, 
        TRAJECTORY_ST, 
        TRAJECTORY_ET, 
        TRAJECTORY_MBR) 
        VALUES (
        {key_value.id},
        '',
        '{key_value.start}',
        '{key_value.end}',
        '{key_value.mbr}')'''
    return sql


def get_insert_key_values_nclob(trajectory_id: int, nclob: str):
    sql = f'''
        UPDATE {DB_TABLE_KEY_VALUE} SET TRAJECTORY_OBJECT=CONCAT(TRAJECTORY_OBJECT, '{nclob}') 
        WHERE TRAJECTORY_ID={trajectory_id})'''
    return sql
