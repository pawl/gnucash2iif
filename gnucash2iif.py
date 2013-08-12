import csv
import re

def CheckDate(dateString):
        '''Checks a date if it is in a valid format'''
        r = re.compile('.*/.*/.*')
        if r.match(dateString) is not None:
            return True
        else:
            return False

with open('generalledger.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        if CheckDate(row[0]):
            print "this is a date"
        else:
            print row
