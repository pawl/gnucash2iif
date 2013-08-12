import csv
import sys
with open(sys.argv[1], 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        print row
