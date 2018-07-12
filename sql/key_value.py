from consts import DB_TABLE_KEY_VALUE
from models.key_value import KeyValue
from pyhdb import NClob


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


def get_insert_key_values_nclob(trajectory_id, nclob: str):
    return f'''
        UPDATE KEY_VALUE SET TRAJECTORY_OBJECT=CONCAT(TRAJECTORY_OBJECT, '{nclob}') 
        WHERE TRAJECTORY_ID={trajectory_id}'''


def get_insert_key_value_trips(key_value: KeyValue):
    return f'''
        INSERT INTO {DB_TABLE_KEY_VALUE} (ID, OBJ, ST, ET, MBR) 
        VALUES ({key_value.id}, '{key_value.obj}', {key_value.start}, {key_value.end}, '{key_value.mbr}')
        '''


def get_insert_key_values_trips_nclob(trajectory_id, nclob: str):
    return f'''
        UPDATE {DB_TABLE_KEY_VALUE} SET OBJ=CONCAT(OBJ, '{nclob}') 
        WHERE ID={trajectory_id}'''
