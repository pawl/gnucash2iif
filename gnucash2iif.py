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
    transactions = []
    for transaction in transactionList:
        transactionHeader = transaction.pop(0)
        trns = {"date": transactionHeader[0], "docnum": transactionHeader[1], "memo": transactionHeader[2], "spl": []}
        splitCount = 0
        for splitTrans in transaction:
            splitCount += 1
            if splitTrans[-2]:
                #remove comma and dollar sign
                #debit
                amount = re.sub("[^\d\.]", "", splitTrans[-2])
            elif splitTrans[-1]:
                #credit
                amount = "-" + re.sub("[^\d\.]", "", splitTrans[-1])
            #quickbooks requires an amount on each line (can't be blank)
            else:
                amount = "0"
            amount = amount.strip(' \t\n\r') # trim whitespace
            if splitTrans[-4]:
                splitMemo = splitTrans[-4]
            else:
                splitMemo = ""
            trns["spl"].append({"amount": amount, "accnt": splitTrans[3],"date": trns["date"], "memo": splitMemo})
        if splitCount > 1:
            transactions.append(trns)
        else:
            print "transaction only had one split:"
            print transaction

header = "!TRNS	TRNSID	TRNSTYPE	DATE	ACCNT	CLASS	AMOUNT	DOCNUM	MEMO\n"\
        + "!SPL	SPLID	TRNSTYPE	DATE	ACCNT	CLASS	AMOUNT	DOCNUM	MEMO\n"\
        + "!ENDTRNS\n"

iif_file = open("output.iif", "w")
iif_file.write(header)
for item in transactions:
    templateTRNS = "TRNS		GENERAL JOURNAL	%(DATE)s	%(ACCNT)s		%(AMOUNT)s	%(DOCNUM)s	%(MEMO)s\n" % {'DATE': item["date"], 'ACCNT': item["spl"][0]["accnt"], 'AMOUNT': item["spl"][0]["amount"], 'DOCNUM': item["docnum"], 'MEMO': item["memo"]}
    iif_file.write(templateTRNS)
    splCount = 0
    for spl in item["spl"]:
        if splCount > 0:
            templateSPL = "SPL		GENERAL JOURNAL	%(DATE)s	%(ACCNT)s		%(AMOUNT)s		%(MEMO)s\n" % {'DATE': spl["date"], 'ACCNT': spl["accnt"], 'AMOUNT': spl["amount"], 'MEMO': spl["memo"]}
            iif_file.write(templateSPL)
        splCount = splCount + 1
    templateEND = "ENDTRNS\n"
    iif_file.write(templateEND)
iif_file.close()
