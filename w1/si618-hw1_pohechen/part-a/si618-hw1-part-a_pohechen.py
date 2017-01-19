
## Step 1 (35 points)  Processing the input file
# (15 points) Read the World Bank country data file (txt)
f = open('world_bank_indicators.txt', 'rU')

# make it a data frame
d = []
try:
    for line in f:
        d.append(line.split('\t'))
finally:
    f.close()

# remove the \n in the end of each row
for i in xrange(len(d)):
    d[i][-1] = d[i][-1][:-1]

# extract out header
header = d[0]
d.pop(0)

# create a copy in case
data = d

# (5 points) Keep only rows with date=2000 or date=2010
d = [i for i in d if int(i[1][-4:]) in [2000, 2010]]

# (5 points) Keep only the following columns:
# ('Country Name', 'Date (should be either 2000 or 2010)', 'Total population', 'Mobile subscribers', 'Health: mortality under-5', 'Internet users per 100 people', 'GDP per capita')
# try using 'pandas' modules
import pandas as pd
d = pd.DataFrame(d, columns = header)
d = d[['Country Name','Date','Population: Total (count)','Business: Mobile phone subscribers','"Health: Mortality, under-5 (per 1,000 live births)"','Business: Internet users (per 100 people)','Finance: GDP per capita (current US$)']]

# convert string into integer after the column of Date and remove commas ','
for i in xrange(2,7):
    d.iloc[:, i] = d.iloc[:, i].str.replace(r',|"','')
    d.iloc[:, i] = pd.to_numeric(d.iloc[:, i])

# remove NaN
d = d.dropna()

# (5 points) Compute and add the following new columns:
d['Mobile subscribers per capita'] = d['Business: Mobile phone subscribers'] / d['Population: Total (count)']

import numpy as np
d['log(GDP per capita)'] = np.log(d['Finance: GDP per capita (current US$)'])
d['log(Health: mortality under 5)'] = np.log(d['"Health: Mortality, under-5 (per 1,000 live births)"'])

# (5 points) Store any numbers in the format of exactly 5 digits after the decimal point (for example 0.00223).
d['Mobile subscribers per capita'] = d['Mobile subscribers per capita'].round(5) 
d['log(GDP per capita)'] = d['log(GDP per capita)'].round(5)
d['log(Health: mortality under 5)'] = d['log(Health: mortality under 5)'].round(5)


## Step 2 (20 points)   Adding regions
# (15 points)  Add code to read the region file (world_bank_regions.txt) into an appropriate data structure.  
# try use pandas to read in world_bank_regions.txt
region = pd.read_table('world_bank_regions.txt', sep = '\t', thousands = ',')
del region['Subregion']     # remove useless column


# clean country name before merge
d['Country Name'] = d['Country Name'].str.replace('"', '')

# (5 points)
d = d.merge(region, left_on='Country Name', right_on='Country', how='left')
del d['Country']

## Step 5 (15 points) Sorting
# (5 points) First sort by ascending year (so that rows with date=2000 should come before rows with date=2010)
# (5 points) Then within each year, sort by region (the usual alphabetic order)
# (5 points) Then within each year and region, sort by increasing GDP per capita
d = d.dropna()
d = d.sort(['Date', 'Region', 'Finance: GDP per capita (current US$)'], ascending = True)

## Step 6 (15 points) Output to a file in CSV format.
d.to_csv('worldbank_output_pohechen.csv', sep = ',', header = True, index = False)

