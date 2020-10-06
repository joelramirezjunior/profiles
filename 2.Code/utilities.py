import csv, numpy
import collections
from collections import Counter


def returnCleanNPArray(fileName, LENAVariable):
    with open(fileName, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        time = []
        value = []
        subject = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1

            time.append(float(row["Time"]))
            value.append(float(row[LENAVariable]))
            subject = row['SUBJECT']
            line_count += 1
        print("Done creating np array with LENA values")
        return subject, numpy.array(time) , numpy.array(value)


def returnClusterMeasures(labels):

    if labels == []:
        return 0,0 
    labels = labels.tolist()
    cntr = collections.Counter(labels)

    return len(Counter(cntr).keys()), numpy.mean(list(Counter(cntr).values()))
