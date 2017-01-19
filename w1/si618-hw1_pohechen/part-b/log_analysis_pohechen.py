# (a) A summary file that contains the counts of all valid daily visits
# to each top-level domain.
# The rows should be ordered in chronological order, and the columns
# should be sorted in alphabetical order of top-level domains.  The 
# file should be tab-delimited.

# read in the log file
with open('access_log.txt', 'rU') as f:
    d = f.read()

# make a smaller sample
# data = d
# d = d#[0:int(len(d)*0.01)]

# load in module of re
import re

### r = re.findall(r'\[(\d{2}\/\w{3}\/\d{4})\:\d{2}:\d{2}:\d{2}\s-0500\]\s\"(?:GET|POST)\s(?:http|https):\/\/(.+?)(?:\/|\s|:).*?\"\s(\d{3}).*?\"\n', d) # original 
r = re.findall(r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\s-\s-\s\[(\d{2}\/\w{3}\/\d{4})\:\d{2}:\d{2}:\d{2}\s-0500\]\s\"(?:GET|POST)\s(?:http|https):\/{2}([^0-9\/\s\.:][a-zA-Z0-9\.\-]+\.\w+)(?::\d+.*|\/.*?|\s|\b)\s*(?:HTTP\/[0-9\.]{3})?\"\s200\s.*?\"\n', d) # 0 difference

### check if all are 200 or not IP address or without any dot 
# for i in list(r):
#     if i[2] != '200' or re.match(r'[0-9]+(?:\.[0-9]+){3}', i[1]) or re.match(r'^[^\.]*$', i[1]) or re.match(r'^\.', i[1]): 
#         r.remove(i)

# remove port part & extract top-level domain
domain = []
for i in r:
    domain.append(re.findall(r'.+\.(.*)', i[1])[0])

time = []
for i in r:
    time.append(i[0])

# check
if len(domain) != len(time): print('lengths are not equal!!')

# make all domain lower case
for i in xrange(len(domain)):
    if not domain[i].islower(): domain[i] = domain[i].lower()

### clean weird empty data
# tmp = []
# for i in xrange(len(domain)):
#     if domain[i] == '': tmp.append(i)

# for i in sorted(tmp, reverse=True):
#     del domain[i]
#     del time[i]

### make weird case (.com"...) normal
# for i in xrange(len(domain)):
#     if re.search(r'"', domain[i]): domain[i] = re.findall(r'(.*?)".*','com" 302 0 "-" "-"')[0]

# make these data a table
import pandas as pd

d = pd.DataFrame(
    {'domain' : domain,
     'visitTime' : time,
    })

# sort by alphabet
## IMPORTANT: http://stackoverflow.com/questions/17071871/select-rows-from-a-dataframe-based-on-values-in-a-column-in-pandas

# write the final out
with open('valid_log_summary_pohechen.txt', 'w') as f:
    for i in d.visitTime.unique():
        tmp = d.loc[d['visitTime'] == i].domain.value_counts()
        output = i + '\t'
        for j in tmp.sort_index().index:
            output = output + j + ':' + str(tmp[j])+'\t'
        output = output + '\n'
        f.write(output)



# (b) A suspicious entries file with the actual invalid access rows
# filtered from the original log, according to the criteria below.

# read in the log file again
with open('access_log.txt', 'rU') as f:
    d = f.read()

## regex: not containing xxx: http://stackoverflow.com/questions/406230/regular-expression-to-match-line-that-doesnt-contain-a-word
# find all valid line of log and remove them from d
# d = re.sub(r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\s-\s-\s\[\d{2}\/\w{3}\/\d{4}\:\d{2}:\d{2}:\d{2}\s-0500\]\s\"(?:GET|POST)\s(?:http|https):\/\/.+?(?:\/|\s|:).*?\"\s\d{3}.*?\"\n', '', d)
# d = re.sub(r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\s-\s-\s\[\d{2}\/\w{3}\/\d{4}\:\d{2}:\d{2}:\d{2}\s-0500\]\s\"(?:GET|POST)\s(?:http|https):\/\/((?![0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}).+?)(?::\d+|\/.*?|\s)\s*HTTP\/[0-9\.]{3}\"\s(200).*?\"\n', '', d)
# d = re.sub(r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\s-\s-\s\[\d{2}\/\w{3}\/\d{4}\:\d{2}:\d{2}:\d{2}\s-0500\]\s\"(?:GET|POST)\s(?:http|https):\/{2}((?![0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}).+?)(?::\d+|\/.*?|\s|\b)\s*(?:HTTP\/[0-9\.]{3})?\"\s(200).*?\"\n', '', d)
# d = re.sub(r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\s-\s-\s\[\d{2}\/\w{3}\/\d{4}\:\d{2}:\d{2}:\d{2}\s-0500\]\s\"(?:GET|POST)\s(?:http|https):\/{2}([^0-9\/]+.+?)(?::\d+|\/.*?|\s|\b)\s*(?:HTTP\/[0-9\.]{3})?\"\s(200).*?\"\n', '', d)
# d = re.sub(r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\s-\s-\s\[\d{2}\/\w{3}\/\d{4}\:\d{2}:\d{2}:\d{2}\s-0500\]\s\"(?:GET|POST)\s(?:http|https):\/{2}([^0-9\/]+.+?)(?::\d+|\/.*?|\s|\b)\s*(?:HTTP\/[0-9\.]{3})?\"\s(200)\s.*?\"\n', '', d)  #12

d = re.sub(r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\s-\s-\s\[\d{2}\/\w{3}\/\d{4}\:\d{2}:\d{2}:\d{2}\s-0500\]\s\"(?:GET|POST)\s(?:http|https):\/{2}([^0-9\/\s\.:][a-zA-Z0-9\.\-]+\.\w+)(?::\d+.*|\/.*?|\s|\b)\s*(?:HTTP\/[0-9\.]{3})?\"\s(200)\s.*?\"\n', '', d) # 0 difference

# write it out!
with open('invalid_access_log_pohechen.txt', 'w') as f:
    f.write(d)
