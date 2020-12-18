import os, re, csv, sys
from g2p_en import G2p

g2p = G2p()

class Name:
    def __init__(self, name, m=0, f=0, phnms='', sibs=None):
        self.name = name
        self.m = m
        self.f = f
        self.phnms = phnms
        if sibs:
            self.sibs = sibs
        else:
            self.sibs = set()

    def __str__(self):
        return f'{self.name} m:{self.m} f:{self.f} phnms:{self.phnms} sibs:{self.sibs}'

    def __repr__(self):
        return f'<{self.name}: m:{self.m}, f:{self.f}, phnms:{self.phnms}, sibs:{self.sibs}>'

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

    def __len__(self):
        return len(self._names)

    def sorted_by_total(self):
        return sorted(list(self._names.values()), key=lambda x: x.total(), reverse=True)

    def sorted_by_neutrality(self):
        return sorted(list(self._names.values()), key=lambda x: abs(x.ratio()), reverse=False)

    def add(self, name, m=0, f=0, sibling=False, phnms=''):
        if name in self:
            self._names[name].m += m
            self._names[name].f += f
            if sibling:
                self._names[name].sibs |= {sibling}
        else:
            self._names[name] = Name(name, m=m, f=f, phnms=''.join(g2p(name)))

    def reduced(self):
        oldest_sibs = {}
        reduced = Name_Collection()
        for name in self.sorted_by_total():
            try:
                reduced.add(oldest_sibs[name.phnms], m=name.m, f=name.f, sibling=name.name)
            except KeyError:
                oldest_sibs[name.phnms] = name.name
                reduced.add(name.name, m=name.m, f=name.f, phnms=name.phnms)
        return reduced

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

def get_neutrality_threshold():
    ratio = -1
    while ratio < 0:
        ratio = input('Enter a neutrality threshold or press q to quit: ')
        if ratio == 'q':
            sys.exit('Goodbye!')
        try:
            if 0 <= float(ratio) <= 1:
                ratio = float(ratio)
            else:
                print('Threshold must be a float from 0 to 1')
                ratio = -1
        except ValueError:
            print('Invalid input, please try again.')
            ratio = -1
    return ratio

def get_batch_size(max):
    num = -1
    while num < 0:
        num = input('Enter how many names to display or press q to quit: ')
        if num == 'q':
            sys.exit('Goodbye!')
        try:
            if 0 <= int(num) <= max:
                num = int(num)
            else:
                print(f'Number must be an int from 0 to {max}')
                num = -1
        except ValueError:
            print('Invalid input, please try again.')
            num = -1
    return num

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
reduced = names.reduced()

while True:
    ratio = get_neutrality_threshold()
    batch_size = get_batch_size(len(names))
    neutral_names = [x for x in reduced.sorted_by_total() if abs(x.ratio()) <= ratio]
    print('')
    for name in neutral_names[0:batch_size]:
        print(f'{name.name} ratio: {abs(name.ratio()):4f} m: {name.m} f: {name.f} total spellings: {len(name.sibs) + 1}')
    print('')
