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

class Name_Collection:
    def __init__(self):
        self._names = {}

    def __getitem__(self, name):
        return self._names[name]

    def __iter__(self):
        return self._names

    def __contains__(self, name):
        out = None
        try:
            self._names[name]
            out = True
        except KeyError:
            out = False
        return out

    def __repr__(self):
        out = '{'
        for name in self._names:
            out += self._names[name].__repr__() + ', '
        if out.endswith(', '):
            out = out[:-2] + '}'
        else:
            out += '}'
        return out

    def add(self, name, m=0, f=0):
        if name in self:
            self._names[name].m += m
            self._names[name].f += f
        else:
            self._names[name] = Name(name, m=m, f=f)

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
