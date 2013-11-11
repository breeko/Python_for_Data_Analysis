import json

path = 'ch02/usagov_bitly_data2012-03-16-1331923249.txt'        # json file
records = [json.loads(line) for line in open(path)]             # list of dictionaries with the json file

time_zones = [rec['tz'] for rec in records if 'tz' in rec]      # take all the time-zones (note that not all records have 'tz')

def get_counts(sequence):
    ''' input: list of values
        output: dictionary of values and their respective counts 
    ''' 
    counts = {}
    for x in sequence:
        if x in counts:
            counts[x] += 1
        else:
            counts[x] = 1
    return counts

from collections import defaultdict

def get_counts2(sequence):
    ''' alternative to get_counts '''
    counts = defaultdict(int)   # values get initialized to 0
    for x in sequence:
        counts[x] += 1
    return counts

time_zones_count = get_counts(time_zones)

def top_counts(count_dict, n = 10):
    ''' returns n largest counts '''
    value_key_pairs = [(count,tz) for tz, count in count_dict.items()]
    value_key_pairs.sort()
    return value_key_pairs[-n:]

# prints top 10 time zones
print top_counts(time_zones_count)

# # Counter from module collections does the same thing
# Only works in Python 2.7+
# from collections import Counter
# counts = Counter(time_zones)
# counts.most_common(10)

from pandas import DataFram, Series
import pandas as pd; import numpy as np

frame = DataFrame(records)
