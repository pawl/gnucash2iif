import csv
import re

def CheckDate(dateString):
    '''Checks a date if it is in a valid format'''
    r = re.compile('.*/.*/.*')
    if r.match(dateString) is not None:
        return True
    else:
        return False

with open('generalledger_raw.csv', 'rb') as f:
    reader = csv.reader(f)
    transactionList = [] #contains list of transactions
    splits = [] #contains components of each transaction
    
    for row in reader:
        #ignore blank rows
        if all(x is '' for x in row):
            continue
        
        #check if row is the beginning of a record
        elif CheckDate(row[0]):
            if len(splits) > 0:
                #add previous transaction to list
                transactionList.append(splits) 
                
                # clear splits and start over
                splits = [] 
                splits.append(row)
            else:
                # no previous transactions
                splits = []
                splits.append(row)

        #row is not beginning of record, add to splits
        else:
            splits.append(row)
    
    print transactionList[0]
