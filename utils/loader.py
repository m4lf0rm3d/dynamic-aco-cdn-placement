import csv

def load_csv(path):
    with open(path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        return [dict(row) for row in reader]