from hana_connector import HanaConnection
import argparse
import os
import json
from datetime import datetime


def fetch_trajectory():
    with HanaConnection() as connection:
        connection.execute(f'''SELECT * FROM TAXI.KEY_VALUE WHERE TRAJECTORY_ID={args.tid}''')
        trajectory = connection.fetchone()
        unpack_values(trajectory)


def unpack_values(trajectory):
    with open(f'''key_value_{args.tid}.csv''', 'w') as f:
        f.write('latitude, longitude, timestamp')
        f.write(os.linesep)
        trajectory[1].read()
        samples = json.loads(str(trajectory[1]))

        for sample in samples:
            f.write(','.join(str(value) for value in get_sample(sample)))
            f.write(os.linesep)


def get_sample(sample):
    print(sample)
    lat = sample[1]
    lon = sample[2]
    date_time = datetime.strptime(sample[0], '%Y-%m-%d %H:%M:%S')
    timestamp = date_time.hour * 60 * 60 + date_time.minute * 60 + date_time.second
    return (lat, lon, timestamp)


def main(args):
    fetch_trajectory()


if __name__ == '__main__':
    '''
    argument parser
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--tid',
        help='trajectory ID required',
        type=int,
        default=None,
        required=False
    )
    args = parser.parse_args()
    main(args)
