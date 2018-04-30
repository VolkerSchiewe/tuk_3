from hana_connector import HanaConnection

with HanaConnection() as connection:
    connection.execute('SELECT * FROM tables')
    result = connection.fetchall()
