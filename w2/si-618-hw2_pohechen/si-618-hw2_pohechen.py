# -- coding: utf-8 --
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')
######### encoding issue ##########
# http://www.ianbicking.org/illusive-setdefaultencoding.html
# http://stackoverflow.com/questions/21129020/how-to-fix-unicodedecodeerror-ascii-codec-cant-decode-byte
###################################
import urllib2

## Step 1
# fetch html from IMDB
url = 'http://www.imdb.com/search/title?at=0&sort=num_votes&count=100'
html = urllib2.urlopen(url).read()

# (10 points) write fetched html into a html file
with open('step1.html', 'w') as f:
    for i in html:
        f.write(i)

# read in step1.html cuz the data keeps changing
with open('step1.html', 'r') as f:
    html = f.read()

## Step2
# parse html page 
from bs4 import BeautifulSoup as bs
soup = bs(html)

# # save them into a txt
import codecs
with codecs.open('step2.txt', 'w', encoding = 'utf-8') as f:
    f.write('IMDB_ID\tRank\tTitle\n')
    for i in soup.find_all('h3')[0:100]:
        rank = i.contents[1].string[:-1]
        title = i.contents[3].string
        imdbId = i.contents[3]['href'].split('/')[2]
        f.write(imdbId + '\t' + rank + '\t' + title + '\n')


## Step3
# read in step2.html
import pandas
import time # to sleep

# d = pandas.read_table('step2.txt', sep = '\t')
# with codecs.open('step3.txt', 'w', encoding = 'utf-8') as f:
#     for i in d.IMDB_ID:
#         url = 'http://omdbapi.com/?i=' + i
#         json_str = urllib2.urlopen(url).read()
#         f.write(json_str + '\n')
#         time.sleep(3) 


## Step 4
import json
import collections

with open('step3.txt', 'r') as f:
    json_str = f.read()

imdbMeta = []
for i in json_str.split('\n')[:-1]:
    tmp = json.loads(i)
    # imdbMeta = imdbMeta +'{\'Title\':' + tmp['Title'] + ', \'Actors\':' + tmp['Actors'].split(', ')[:5] + ',}'
    # print imdbMeta
    
    imdbMeta.append(collections.OrderedDict([('Title', tmp['Title']), ('Actors', tmp['Actors'].split(', ')[:5])]))
# imdbMeta = imdbMeta + ']'

with open('step4.json', 'w') as f:
    json.dump(imdbMeta, f)


## Step 5
import pydot
import itertools
with open('step4.json', 'r') as f:
    d = json.loads(f.read())

# first you create a new graph, you do that with pydot.Dot()
g = pydot.Dot(graph_type = 'graph')    
for i in d:
    for x,y in itertools.combinations(i['Actors'], 2):
        e = pydot.Edge(x, y)
        g.add_edge(e)

g.write('actors_graph_output.dot')
g.write_png('actors_graph.png')

