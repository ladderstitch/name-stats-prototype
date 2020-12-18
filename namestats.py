import os, re, csv, sys

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

    def total(self):
        return self.m + self.f

    def ratio(self):
        # ratio of people with each gender marker,
        # where -1 is 100% m and 1 is 100% f
        return (self.f - self.m) / self.total()

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

def get_year_range(years):
    print(f'Data available for years {years[0]} - {years[-1]}.')
    first_year = -1
    while int(first_year) not in years:
        first_year = input('Enter the first year or press q to quit: ')
        if first_year == 'q':
            sys.exit('Goodbye!')
        try:
            if int(first_year) in years:
                first_year = int(first_year)
            else:
                print('No data for selected year.')
                first_year = -1
        except ValueError:
            print('Invalid input, please try again.')
            first_year = -1

    last_year = -1
    while int(last_year) not in years:
        last_year = input('Enter the last year or press q to quit: ')
        if last_year == 'q':
            sys.exit('Goodbye!')
        try:
            if int(last_year) in years:
                last_year = int(last_year)
                if last_year < first_year:
                    print('Last year cannot be less than first year. Please try again')
                    last_year = -1
            else:
                print('No data for selected year.')
                last_year = -1
        except ValueError:
            print('Invalid input, please try again.')
            last_year = -1

    print(f'range {first_year} to {last_year}')
    return (first_year, last_year)

list_of_files = os.listdir('./data')

years = []

for file in list_of_files:
    if file[0] != "." and len(file) > 0:
        years.append(int(re.match('yob(\d+)\.txt', file).group(1)))
years = sorted(years)

year_range = get_year_range(years)

names = Name_Collection()

for year in range(year_range[0], year_range[1] + 1):
    with open(f'./data/yob{year}.txt') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if row[1].lower() == 'm':
                names.add(row[0], m=int(row[2]))
            elif row[1].lower() == 'f':
                names.add(row[0], f=int(row[2]))
            else:
                raise ValueError('Unexpected gender marker')


print(names)
