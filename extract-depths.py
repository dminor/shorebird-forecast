import pandas as pd

dates = []
depths = []

with open('data/Daily__Jan-19-2019_03_49_07PM.csv', 'r') as f:
    # skip first line, headers start at line 2
    f.readline()

    first = True
    headers = {}
    for line in f:
        fields = line.strip().split(',')
        if first:
            for i, field in enumerate(fields):
                headers[field] = i
            first = False
            continue

        # limit to water depth observations
        if fields[headers['PARAM']] != '2':
            continue

        # limit to observations from 2012 and later
        if int(fields[headers['Date']].split('/')[0]) <= 2011:
            continue

        dates.append(fields[headers['Date']])
        depths.append(fields[headers['Value']])

df = pd.DataFrame({'date': dates,
                   'depth': depths})

df.to_csv('depths.csv', index=False)
