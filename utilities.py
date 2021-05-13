import csv, numpy
import collections
import numpy as np
import os
from collections import Counter

def getTruth(string):

    if string == 'yes' or string == "y" or string == "Y":
        return True
    elif string == 'no' or string == "n" or string == "N":
        return False
    else:
        str = input("Please put in the correct value, y/n")
        getTruth(str)

def getDemographic(string):
    lang = string
    lang = lang.lower()

    if lang == 'spanish' or lang == "s":
        return 'spanish'
    elif lang == 'english' or lang == "e":
        return 'english'
    else:
        getDemographic(input("Is this Spanish or English? (s/e)"))

def returnCleanNPArray(fileName, LENAVariable):
    with open(fileName, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        time = []
        value = []
        subject = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1

            time.append(float(row["Time"]))
            value.append(float(row[LENAVariable]))
            subject = row['SUBJECT']
            line_count += 1
        return subject, numpy.array(time) , numpy.array(value)


def returnClusterMeasures(labels, values):

    if labels == []:
        return 0,0,0,0,0
    labels = labels.tolist()
    cntr = collections.Counter(labels)


    clus = labels[0]
    size = 0
    clusterSize = []

    for lab, val in zip(labels, values.tolist()):
        if clus != lab:
            clus = lab
            clusterSize.append(size)
            size = 0
        size += val

    clusterSize.append(size)
    print("Done with Measures!")
    return len(Counter(cntr).keys()), numpy.mean(list(Counter(cntr).values())), numpy.min(clusterSize), numpy.max(clusterSize), numpy.mean(clusterSize)



def gini(array):
    """Calculate the Gini coefficient of a numpy array."""
    # based on bottom eq:
    # http://www.statsdirect.com/help/generatedimages/equations/equation154.svg
    # from:
    # http://www.statsdirect.com/help/default.htm#nonparametric_methods/gini.htm
    # All values are treated equally, arrays must be 1d:
    array = array.flatten()
    if np.amin(array) < 0:
        # Values cannot be negative:
        array -= np.amin(array)
    # Values cannot be 0:
    array += 0.0000001
    # Values must be sorted:
    array = np.sort(array)
    # Index per array element:
    index = np.arange(1,array.shape[0]+1)
    # Number of array elements:
    n = array.shape[0]
    # Gini coefficient:
    return ((np.sum((2 * index - n  - 1) * array)) / (n * np.sum(array)))



dir = "Spanish_Dataset/Habla_3.0_L1_Pre_All_Day"

def changeXLXtoCSV(dir):
    for file in os.listdir(dir):
        print(file)
        path = os.path.join(dir, file)
        name = file.split('.')
        name.pop(-1)
        name = ".".join(name)
        target = os.path.join(dir, name + '.csv')
        os.rename(path, target)


# Made to fix the Time and Date error in SOT NEW csv
# import csv
#
# with open('SOT_NEW16FIXED.csv', mode='w') as sotfixed:
#     sot_writer = csv.writer(sotfixed, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#
#     with open('TL3Data/SOT_NEW16.csv', newline='') as csvfile:
#         reader = csv.reader(csvfile)
#
#         for row in reader:
#             if row[5] == row[6]:
#                 print('both empty')
#             elif row[5] == '' :
#                 print("Date Fixed")
#                 date, time = row[6].split()
#                 time = time.split(':')[0] + '.' + time.split(':')[1]
#                 row[5] = date
#                 row[6] = time
#
#             elif row[6] == '' :
#                 print("Time Fixed")
#                 date, time = row[5].split()
#                 time = time.split(':')[0] + '.' + time.split(':')[1]
#                 row[5] = date
#                 row[6] = time
#             sot_writer.writerow(row)


def changeXLXtoCSV(dir):
    for file in os.listdir(dir):

        path = os.path.join(dir, file)
        name = file.split('.')
        name.pop(-1)
        name = ".".join(name)
        target = os.path.join(dir, name + '.csv')
        os.rename(path, target)

# Made to fix the Time and Date error in SOT NEW csv
def fixTimeDateError():
    with open('analysisTidySpanishDataset.csv', mode='w') as csvFixed:
        csv_writer = csv.writer(csvFixed, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        with open('tidySpanishDataset.csv', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for i, row in enumerate(reader):

                if i > 0:
                    time = row[5]
                    print(time)
                    print(row)
                    hour, min = time.split(":")
                    time = hour + '.' + min
                    row[5] = time

                csv_writer.writerow(row)
