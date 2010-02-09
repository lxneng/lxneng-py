rows = []
rows.append(['vanessa', 'carlton'])
rows.append(['nelly', 'furtado'])
 
import csv
csv.register_dialect('mycsv', quoting = csv.QUOTE_ALL)
writer = csv.writer(open("file.csv", "wb"), 'mycsv')
 
writer.writerows(rows)
