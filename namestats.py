import os, re

class Name:
    def __init__(self, name, m, f):
        self.name = name
        self.m = m
        self.f = f

    def __str__(self):
        return f'{self.name} m:{self.m} f:{self.f}'

list_of_files = os.listdir('./data')

years = []

for file in list_of_files:
    if file[0] != "." and len(file) > 0:
        years.append(int(re.match('yob(\d+)\.txt', file).group(1)))
years = sorted(years)

first_year = input('Enter the first year: ')
last_year = input('Enter the last year: ')

print(f'range {first_year} to {last_year}')
