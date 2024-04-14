import csv

def readCSV(filename):
    array = []
    with open(filename, 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            array.append(row)
    
    return(array)