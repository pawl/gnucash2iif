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
    for x in range(0, 3):
        reader.next() #skip header lines
    
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

    #get information from transactions and add to dictionary
    for transaction in transactionList:
        transactionHeader = transaction.pop(0)
        trns = {"date": transactionHeader[0], "docnum": transactionHeader[1], "memo": transactionHeader[2], "trnstype": "GENERAL JOURNAL", "spl": []}
        for splitTrans in transaction:
            if splitTrans[-2]:
                #remove comma and dollar sign
                amount = re.sub("[^\d\.]", "", splitTrans[-2])
            if splitTrans[-1]:
                amount = "-" + re.sub("[^\d\.]", "", splitTrans[-1])
            trns["spl"].append({"amount": amount, "accnt": splitTrans[3]})
        print trns
