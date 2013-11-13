import json

path = 'usagov_bitly_data2012-03-16-1331923249.txt'        	# json file
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

from pandas import DataFrame, Series
import pandas as pd; import numpy as np

frame = DataFrame(records)
# printing a frame will give you a summary of the Data Frame
# attributes in a Data Frame can be accessed by name
tz = frame['tz']
# counts of a series can be accessed by using value_counts()
tz_counts = frame['tz'].value_counts()
# fillna function can replace missing (NA) values with unknown (empty strings)
clean_tz = tz.fillna("Missing")
clean_tz[clean_tz == ""] = "Unknown"
tz_counts = clean_tz.value_counts()

# plotting
tz_counts[:10].plot(kind="barh",rot=0)

# create a series based on the first letter of the field 'a'
results = Series([x.split()[0] for x in frame.a.dropna()])

# exclude records with null values in parameter 'a'
cframe = frame[frame.a.notnull()]
operating_system = np.where(cframe['a'].str.contains('Windows'), 'Windows', 'Not Windows')

# pivot on timezone, count of  operating system
by_tz_os = cframe.groupby(['tz',operating_system])
agg_counts = by_tz_os.size().unstack().fillna(0)
# select top overall time zones by constructing an indirect index array from row counts in agg_counts
indexer = agg_counts.sum(1).argsort()

count_subset = agg_counts.take(indexer)[-10:]
# plot bar graph of operating system by time zone
count_subset.plot(kind='barh',stacked=True)
# plot relative bar graph of operating system by time zone
normed_subset = count_subset.div(count_subset.sum(1), axis=0)
normed_subset.plot(kind='barh', stacked=True)



