gnucash2iif
===========

Converts a Gnucash general ledger to an IIF file (for quickbooks)

Instructions (proposed workflow):

1. Create a General Ledger report in Gnucash. (Reports -> Assets and Liabilities -> General Ledger)
2. Save the report as HTML
3. Open the HTML with Excel
4. Remove the completely blank rows using ASAP utilities (the script could easily do this)
5. Save as CSV
6. Run the script using the filename as an argument
