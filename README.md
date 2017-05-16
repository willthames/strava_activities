# Strava activities summariser

## Installation

```
git clone https://github.com/willthames/strava
cd strava
pip install -r requirements.txt
```

## Configuration

See http://strava.github.io/api/ for how to create an access token.
While creating an API application will generate a client ID and a client
secret token, you only need the access token

Create a file called strava.config next to activities.py, and add the access token:
```
access_token=abcd1234...
```

## Obtain records

Run activities.py with an argument of the directory in which you wish to store your data

```
python activities.py data
```

Note that activities.py will pick up where it left off, only downloading files more recent than the latest file in data.

## Summarising results

Filter by year:
```
python recordfilter.py data year=2017 type=run
```

Filter by year, group by month:
```
python recordfilter.py data year=2017 groupby=month type=run
```

Show yearly stats:
```
python recordfilter.py data groupby=year type=run
```

## Eddington Number

Your Eddington Number is the number of days E on which you have done more than E units of distance. As Eddington was British and a cyclist, he used miles. The `eddington.py`
script prints out your Eddington number for both kms and miles

```
python eddington.py data type=run
```

Alternatively, you can just use [`jq`](https://stedolan.github.io/jq/) along with `awk` and `sort`:

```
cd data
# Run miles
jq  -s '[.[] | select(.type=="Run") | .distance/1602.5] | .[] ' * | sort -nr | awk '(NR > $1) { print prev; exit } { prev=NR }'
# Run kms
jq  -s '[.[] | select(.type=="Run") | .distance/1000] | .[] ' * | sort -nr | awk '(NR > $1) { print prev; exit } { prev=NR }'
# Ride miles
jq  -s '[.[] | select(.type=="Ride") | .distance/1602.5] | .[] ' * | sort -nr | awk '(NR > $1) { print prev; exit } { prev=NR }'
# Ride kms
jq  -s '[.[] | select(.type=="Ride") | .distance/1000] | .[] ' * | sort -nr | awk '(NR > $1) { print prev; exit } { prev=NR }'
```
