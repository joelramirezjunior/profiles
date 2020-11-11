# Gini
# Author: Joel Ramirez Jr.
# ------------------------
# V 1.0

import matplotlib.pyplot as plt
import csv, collections, math, numpy
import random
import glob
from numpy import genfromtxt
from utilities import returnCleanNPArray, returnClusterMeasures, gini

path = "TotalSubLenaVals/*.csv"

giniCoefficiants = []

#Iterating through all Subjects in the path above, here we grab each respective
#participants AWC above their respective 70th percentile
for fname in glob.glob(path):

    subject, time, value = returnCleanNPArray(fname, "AWC")
    ginNum = gini(value)
    print(ginNum)
    giniCoefficiants.append([subject, ginNum])


with open('giniCoef.csv', 'w') as csvfile:

    csvwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

    header = ['SUBJECT', 'gini']

    csvwriter.writerow(header)

    for i in giniCoefficiants:

        sub = i[0]
        gini = i[1]

        csvwriter.writerow([sub, gini])
