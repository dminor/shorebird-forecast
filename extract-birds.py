import gzip
import math

import pandas as pd


# Locations of interest
LOCATIONS = [
    ('Andrew Haydon Park', math.radians(45.3527032), math.radians(-75.812906)),
    ('Carp River Reclamation Area', math.radians(45.3113862), math.radians(-75.9366202)),
    ('Champlain Bridge', math.radians(45.405), math.radians(-75.755)),
    ('Petrie Island', math.radians(45.5029782), math.radians(-75.4917383)),
    ('Shirley\'s Bay', math.radians(45.3746843), math.radians(-75.8909583)),
]


# Radius around location for which we are interested in observations
RADIUS = 1000


def haversine(lat1, lng1, lat2, lng2):
    """ Use Haversine formula to calculate distance between two points"""
    r = 6371000.0 # radius of Earth
    return 2*r*math.sqrt(math.asin(math.sin(0.5*(lat2-lat1))**2 +
                                   math.cos(lat1)*math.cos(lat2)*
                                   math.sin(0.5*(lng2-lng1))**2))

names = []
counts = []
lats = []
lons = []
dates = []
locations = []
records = 0

with gzip.open('data/ebd_relMay-2018.txt.gz', 'rb') as f:
    first = True
    headers = {}
    for line in f:
        fields = line.decode('utf8').strip().split('\t')
        if first:
            for i, field in enumerate(fields):
                headers[field] = i
            first = False
            continue
        records += 1
        if records % 1000 == 0:
            print(records)

        # Restrict to Ottawa / Outaouais
        if not fields[headers['COUNTY CODE']] in ['CA-ON-OT', 'CA-QC-OU']:
            continue

        lat = math.radians(float(fields[headers['LATITUDE']]))
        lng = math.radians(float(fields[headers['LONGITUDE']]))

        for location in LOCATIONS:
            r = haversine(location[1], location[2], lat, lng)

            if r < RADIUS:
                names.append(fields[headers['COMMON NAME']])
                counts.append(fields[headers['OBSERVATION COUNT']])
                lats.append(fields[headers['LATITUDE']])
                lons.append(fields[headers['LONGITUDE']])
                dates.append(fields[headers['OBSERVATION DATE']])
                locations.append(location[0])

print(records)

df = pd.DataFrame({'name': names,
              'count': counts,
              'latitude': lats,
              'longitude': lons,
              'date': dates,
              'location': locations})

df.to_csv('ebird.csv', index=False)
