import os, re, csv

class Name:
    def __init__(self, name, m=0, f=0):
        self.name = name
        self.m = m
        self.f = f

    def __str__(self):
        return f'{self.name} m:{self.m} f:{self.f}'

    def __repr__(self):
        return f'<{self.name}: m:{self.m}, f:{self.f}>'

    def __eq__(self, x):
        if x.isinstance(Name):
            return self.name == x.name
        else:
            return self.name == x

list_of_files = os.listdir('./data')

years = []

for file in list_of_files:
    if file[0] != "." and len(file) > 0:
        years.append(int(re.match('yob(\d+)\.txt', file).group(1)))
years = sorted(years)

first_year = int(input('Enter the first year: '))
last_year = int(input('Enter the last year: '))

print(f'range {first_year} to {last_year}')

names = {}

for year in range(first_year, last_year + 1):
    with open(f'./data/yob{year}.txt') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        names[year] = {}
        for row in csv_reader:
            names[year][row[0]] = int(row[2])

print(names)
