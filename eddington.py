import json
import numericalunits as nu
import numpy as np
import os
import pandas as pd
import sys

COLUMNS = ['start_date_local', 'distance', 'type']

def read_dir_json(dirname):
    records = list()
    for filename in os.listdir(dirname):
        with open(os.path.join(dirname, filename)) as f:
            records.append(json.loads(f.read()))
    df = pd.DataFrame(records, columns=COLUMNS)
    df = df.rename(columns={'distance': 'distance (km)'})
    df['distance (km)'] = df['distance (km)'] * nu.m / nu.km
    df = df.assign(distance_mi=df['distance (km)'] * nu.km / nu.mile)
    df = df.rename(columns={'distance_mi': 'distance (miles)'})
    return df


def apply_filters(filters, data):
    if 'type' in filters:
        data = data[data['type'].str.lower() == filters['type'].lower()]
    return data


def main(args):
    filters = dict()
    for arg in args[1:]:
        if '=' in arg:
            (k, v) = arg.split('=')
            filters[k] = v
        else:
            data = read_dir_json(arg)

    df = apply_filters(filters, data)
    df = df.sort_values('distance (km)', ascending=False)
    df = df.reset_index(drop=True)
    print "km:", df[df['distance (km)'] > df.index+1].count()[0]
    print "mi:", df[df['distance (miles)'] > df.index+1].count()[0]


if __name__ == '__main__':
    sys.exit(main(sys.argv))
