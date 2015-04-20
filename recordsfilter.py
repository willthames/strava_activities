import json
import numericalunits as nu
import numpy as np
import os
import pandas as pd
import sys

COLUMNS = ['start_date_local', 'distance', 'type', 'elapsed_time', 'total_elevation_gain']

def read_dir_json(dirname):
    records = list()
    for filename in os.listdir(dirname):
        with open(os.path.join(dirname, filename)) as f:
            records.append(json.loads(f.read()))
    df = pd.DataFrame(records, columns=COLUMNS)
    df = df.set_index(pd.DatetimeIndex(df['start_date_local']))
    df = df.rename(columns={'elapsed_time': 'duration (hours)', 
        'total_elevation_gain': 'ascent (m)', 
        'distance': 'distance (km)'})
    df['distance (km)'] = df['distance (km)'] * nu.m / nu.km
    df['duration (hours)'] = df['duration (hours)'] * nu.s / nu.hour
    return df


def apply_filters(filters, data):
    if 'month' in filters:
        if not 'year' in filters:
            print "A month filter must have an associated year"
            sys.exit(1)
        else:
            data = data[filters['year'] + '-' + filters['month']]
    elif 'year' in filters:
        data = data[filters['year']]
    if 'type' in filters:
        data = data[data['type'].str.lower() == filters['type'].lower()]
    if 'groupby' in filters:
        if filters['groupby'] == 'month':
            #return data.groupby([data.index.month, data.index.year])
            return data.groupby(pd.Grouper(freq='1M'))
        if filters['groupby'] == 'year':
            return data.groupby([data.index.year])
        return data.groupby[filters['groupby']]
    return data


def main(args):
    filters = dict()
    for arg in args[1:]:
        if '=' in arg:
            (k, v) = arg.split('=')
            filters[k] = v
        else:
            data = read_dir_json(arg)

    grouped = apply_filters(filters, data)
    print grouped.aggregate(np.sum)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
