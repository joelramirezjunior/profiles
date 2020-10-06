# Made to fix the Time and Date error in SOT NEW csv
import csv

with open('SOT_NEW16FIXED.csv', mode='w') as sotfixed:
    sot_writer = csv.writer(sotfixed, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    with open('TL3Data/SOT_NEW16.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)

        for row in reader:
            if row[5] == row[6]:
                print('both empty')
            elif row[5] == '' :
                print("Date Fixed")
                date, time = row[6].split()
                time = time.split(':')[0] + '.' + time.split(':')[1]
                row[5] = date
                row[6] = time

            elif row[6] == '' :
                print("Time Fixed")
                date, time = row[5].split()
                time = time.split(':')[0] + '.' + time.split(':')[1]
                row[5] = date
                row[6] = time
            sot_writer.writerow(row)
