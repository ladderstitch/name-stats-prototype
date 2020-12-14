import os, re

list_of_files = os.listdir('./data')

years = set()

for file in list_of_files:
    if file[0] != "." and len(file) > 0:
        years |= {int(re.match('yob(\d+)\.txt', file).group(1))}
years = sorted(years)

print(years)
