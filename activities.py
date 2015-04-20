from datetime import datetime
import dateutil.parser
import json
import os
import requests
import sys

def get_config():
    cf = open('strava.config')
    config = { k: v for (k, v) in (line.strip().split('=') for line in cf)}
    return config


def get_activities(config, after=0):
    num = 0
    results = []
    while True:
        r = requests.get('https://www.strava.com/api/v3/athlete/activities',
                headers=dict(Authorization='Bearer %s' % config.get('access_token')),
                data=dict(after=after, per_page=200, page=num))
        latest = json.loads(r.text)
        if not latest:
            break
        results.extend(latest)
        num = num + 1
    return results


def main(args):
    config = get_config()
    outputdir = args[1]
    last = 0
    if os.path.exists(outputdir):
        entries = os.listdir(outputdir)
        if entries:
            last = long(sorted(entries)[-1].replace('.json', ''))
    else:
        os.mkdir(outputdir)
    activities = get_activities(config, after=last+1)
    for activity in activities:
        if type(activity) != dict:
            continue
        start_date = dateutil.parser.parse(activity['start_date'])
        start_date = start_date.replace(tzinfo=None) - start_date.utcoffset()
        seconds_since_epoch = (start_date - datetime(1970, 1, 1)).total_seconds()
        filename = os.path.join(args[1], str(int(seconds_since_epoch)) + '.json')
        with open(filename, 'w') as f:
            f.write(json.dumps(activity))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
