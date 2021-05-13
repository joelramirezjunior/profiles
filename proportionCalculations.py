import csv, numpy, collections, math
from numpy import genfromtxt


def truncate(number, decimals=0):
    """
    Returns a value truncated to a specific number of decimal places.
    """
    if not isinstance(decimals, int):
        raise TypeError("decimal places must be an integer.")
    elif decimals < 0:
        raise ValueError("decimal places has to be 0 or more.")
    elif decimals == 0:
        return math.trunc(number)

    factor = 10.0 ** decimals
    return math.trunc(number * factor) / factor

def getSubjectList(dist, subjectList, subPos):
    """
    Returns a list of subject numbers.
    """

    subjects = set()


    for i in range(1, len(dist)):
        subject = float(dist[i][subPos])
        if subject not in subjects:
            subjectList.append(subject)
            subjects.add(subject)

    return subjectList



def createSubjectDict(subjectList, numCols):
    """
    Returns a dictionary that maps from
                 > AWC  [empty]
                /
    SUBJECT ->  -> CTC  [empty]
                \
                 > CVC  [empty]
    """
    subjectDict = dict()
    for s in subjectList:
        subjectDict[s] = dict()


    for sub in subjectDict.keys():
        #24 for either each hour bin, or 288 for each 5 min segment in the day

        #-1 values are those which are empty or null, if there are values in the
        #rows with values other than -1 are values LENA gave
        subjectDict[sub]["awc"] = [-1] * numCols
        subjectDict[sub]["ctc"] = [-1] * numCols
        subjectDict[sub]["cvc"] = [-1] * numCols
    return subjectDict


def subjectDictDataInsertion(diction, dist, subjectIndex, awcIndex, ctcIndex, cvcIndex, hourBinIndex):
    """
    Returns a dictionary that maps from
                 > AWC  [empty]
                /
    SUBJECT ->  -> CTC  [empty]
                \
                 > CVC  [empty]
    """
    for row in dist:
        print(row)
        subject = float(row[subjectIndex])
        hourBin = 0

        if hourBinIndex != 1:
            hourBin =  float(row[hourBinIndex])
        else:
            hourBin =  int(row[hourBinIndex])

        time = hourBin

        awc = float(row[awcIndex])
        ctc = float(row[ctcIndex])
        cvc = float(row[cvcIndex])

        if hourBinIndex != 1:
            frac, whole = math.modf(hourBin)

            if frac != 0:
                hourBin = (whole)*12 + frac*20
            else:
                hourBin = (whole)*12
            hourBin = int(round(hourBin))

        print("This is the time:", hourBin)
        diction[subject]["awc"][hourBin] = awc
        diction[subject]["ctc"][hourBin] = ctc
        diction[subject]["cvc"][hourBin] = cvc
    return diction


def findProportions(subjectDict, subjectDictSeg, subjectList, flag):

    subjPropHourly = {}
    subjPropSeg = {}

    if flag == 'ordered':

        #first hourly

        subjPropHourly = {}
        subjPropSeg = {}
        for subject in subjectList:

            # subjPropHourly[subject] = {}
            subjPropSeg[subject] = {}

            # propListHourly = [-1]*24
            propListSeg =  [-1] * 288

            #unordered AWC list
            # awcList = subjectDict[subject]['awc']
            awcListSeg = subjectDictSeg[subject]['awc']
            #ordered indecis for AWC
            # sortedHours = sorted(range(len(subjectDict[subject]['awc'])), key=lambda k: subjectDict[subject]['awc'][k], reverse=True)
            sortedSegemnts = sorted(range(len(subjectDictSeg[subject]['awc'])), key=lambda k: subjectDictSeg[subject]['awc'][k], reverse=True)

            # subjPropHourly[subject]['hours'] = sortedHours
            # subjPropHourly[subject]['prop'] = propListHourly

            subjPropSeg[subject]['segments'] = sortedSegemnts
            subjPropSeg[subject]['prop'] = propListSeg

            # for i in range(1, len(sortedHours)):
            #
            #     if subjectDict[subject]['awc'][sortedHours[i]] > 0 :
            #         subjPropHourly[subject]['prop'][i-1] = subjectDict[subject]['awc'][sortedHours[i]] / subjectDict[subject]['awc'][sortedHours[i-1]]
            #     else:
            #         break

            for i in range(1, len(sortedSegemnts)):

                if subjectDictSeg[subject]['awc'][sortedSegemnts[i]] > 0 :
                    subjPropSeg[subject]['prop'][i-1] = subjectDictSeg[subject]['awc'][sortedSegemnts[i]] / subjectDictSeg[subject]['awc'][sortedSegemnts[i-1]]
                else:
                    break

    return subjPropHourly, subjPropSeg



def createDictCSV(dictionary, subjectList, type):

    if type == 'hourly_prop':
        with open('hourlyProportionsEnglish.csv', 'w') as csvfile:

            spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            header = ['subject', 'prop', 'hour']
            spamwriter.writerow(header)

            for sub in subjectList:
                #spamwriter.writerow(['subject', 'prop', 'hour'])
                propList = dictionary[sub]['prop']
                hourList = dictionary[sub]['hours']
                for prop, hour in zip(propList, hourList):
                    if prop == -1:
                        continue
                    prop = truncate(prop, 3)
                    spamwriter.writerow([sub, prop, hour])


    if type == 'seg_prop':
        with open('segProportionsEnglish.csv', 'w') as csvfile:

            spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            header = ['subject', 'prop', 'time']
            spamwriter.writerow(header)

            for sub in subjectList:
                #spamwriter.writerow(['subject', 'prop', 'hour'])
                propList = dictionary[sub]['prop']
                segList = dictionary[sub]['segments']
                for prop, seg in zip(propList, segList):

                    decimal = seg%12
                    time = 0
                    if decimal == 0:
                        time =  seg//12
                    else:
                        time = seg//12 + .05*decimal
                    if prop == -1:
                        continue
                    prop = truncate(prop, 3)
                    spamwriter.writerow([sub, prop, time])


    if type == 'hourly_ordered':
        with open('hourlyOrdredAwc16English.csv', 'w') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            header = ['Subject', 'AWC', 'hour']
            csvwriter.writerow(header)
            for sub in subjectList:
                #unordered AWC list
                awcList = dictionary[sub]['awc']
                #ordered indecis for AWC
                sortedHours = sorted(range(len(dictionary[sub]['awc'])), key=lambda k: dictionary[sub]['awc'][k], reverse=True)

                for ind in sortedHours:
                    awc = dictionary[sub]['awc'][ind]
                    csvwriter.writerow([sub, awc, ind])

    if type == 'seg_ordered':
        with open('segOrdredAwc16English.csv', 'w') as csvfile:

            csvwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            header = ['Subject', 'AWC', 'hour']
            csvwriter.writerow(header)

            for sub in subjectList:
                #unordered AWC list
                awcList = dictionary[sub]['awc']

                #ordered indecis for AWC
                sortedTime = sorted(range(len(dictionary[sub]['awc'])), key=lambda k: dictionary[sub]['awc'][k], reverse=True)

                for ind in sortedTime:

                    awc = dictionary[sub]['awc'][ind]
                    decimal = ind%12
                    time = 0
                    if decimal == 0:
                        time =  ind//12
                    else:
                        time = ind//12 + .05*decimal
                    csvwriter.writerow([sub, awc, time])


def main():
    # distSumHourly = genfromtxt("1.Data Restructuring/English_Dataset/processedData/EnglishHourly.csv", delimiter=',')
    distSumSegment= genfromtxt("1.Data Restructuring/englishCDS.csv", delimiter=',')

    #the first row is full of NA values, thus we are removing them
    # distSumHourly = distSumHourly[1:]
    #
    subjectDict = dict()
    subjectList = []
    #
    subjectList = getSubjectList(distSumSegment, subjectList, 12)
    # subjectDict = createSubjectDict(subjectList, 24)
    #
    # subjectDictHourly = subjectDictDataInsertion(subjectDict, distSumHourly, 0, 6, 7, 8, 1)

    distSumSegment = distSumSegment[1:]
    subjectDictSeg = dict()
    subjectDictSeg = createSubjectDict(subjectList, 288)
    subjectDictSeg = subjectDictDataInsertion(subjectDictSeg, distSumSegment,12, 1, 2, 3, 13)

    subjPropHourly, subjPropSeg = findProportions(subjectDict, subjectDictSeg, subjectList, 'ordered')

    # createDictCSV(subjPropHourly, subjectList, 'hourly_prop')
    createDictCSV(subjPropSeg, subjectList, 'seg_prop')

    # createDictCSV(subjectDict, subjectList, 'hourly_ordered')
    createDictCSV(subjectDictSeg, subjectList, 'seg_ordered')





if __name__ == "__main__":
    main()
