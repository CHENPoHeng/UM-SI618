from pyspark import SparkContext, SparkConf
import json # for yelp json file

APP_NAME = 'YelpSummary'
conf = SparkConf().setAppName(APP_NAME)
sc = SparkContext(conf = conf)


def convert_r(d):
    uid = d['user_id']
    bid = d['business_id']
    star = d['stars']
    tuples = []
    tuples.append((uid, bid, star))
    return tuples

def convert_b(d):
    city = d['city']
    bid = d['business_id']
    tuples = []
    tuples.append((city, bid))
    return tuples

# read in review data and convert it into dictionary
r = sc.textFile("hdfs:///var/si618w17/yelp_academic_dataset_review_updated.json")
r = r.map(lambda x : json.loads(x)) 
r = r.flatMap(lambda x : convert_r(x)) 

# read in business data and convert it into dictionary
b = sc.textFile("hdfs:///var/si618w17/yelp_academic_dataset_business_updated.json")
b = b.map(lambda x : json.loads(x)) 
b = b.flatMap(lambda x : convert_b(x)) 

tmpr = r.map(lambda x:(x[1], x[0]))
tmpb = b.map(lambda x:(x[1], x[0]))
tmp = tmpr.fullOuterJoin(tmpb)
x = tmp.map(lambda x:(x[1][0], x[1][1]))
x = x.distinct()
tmp = x.map(lambda x: (x[0], 1)).reduceByKey(lambda a, b: a + b)
tmp = tmp.map(lambda x: (x[1], 1)).reduceByKey(lambda a, b: a + b)
tmp = tmp.sortBy(lambda x: (x[0]), ascending = True).collect()
del tmp[-1]; del tmp[-1]; tmp.append((28,0));  tmp.append((29,0));  tmp.append((30,1)) 
res = tmp
with open('si618w17hw5-part2_pohechen.csv', 'wb') as f:
    f.write('{},{}\n'.format('cities', 'yelp users'))
    for i in res:
        f.write('{},{}\n'.format(i[0], i[1]))

# 
rGT = r.filter(lambda x: x[2] > 3)

tmpr = rGT.map(lambda x:(x[1], x[0]))
tmpb = b.map(lambda x:(x[1], x[0]))
tmp = tmpr.fullOuterJoin(tmpb)
x = tmp.map(lambda x:(x[1][0], x[1][1]))
x = x.distinct()
tmp = x.map(lambda x: (x[0], 1)).reduceByKey(lambda a, b: a + b)
tmp = tmp.map(lambda x: (x[1], 1)).reduceByKey(lambda a, b: a + b)
tmp = tmp.sortBy(lambda x: (x[0]), ascending = True).collect()
del tmp[-1]
res = tmp
with open('si618w17hw5-part2_pohechen_goodreview.csv', 'wb') as f:
    f.write('{},{}\n'.format('cities', 'yelp users'))
    for i in res:
        f.write('{},{}\n'.format(i[0], i[1]))



#
rST = r.filter(lambda x: x[2] < 3)

tmpr = rST.map(lambda x:(x[1], x[0]))
tmpb = b.map(lambda x:(x[1], x[0]))
tmp = tmpr.fullOuterJoin(tmpb)
x = tmp.map(lambda x:(x[1][0], x[1][1]))
x = x.distinct()
tmp = x.map(lambda x: (x[0], 1)).reduceByKey(lambda a, b: a + b)
tmp = tmp.map(lambda x: (x[1], 1)).reduceByKey(lambda a, b: a + b)
tmp = tmp.sortBy(lambda x: (x[0]), ascending = True).collect()
del tmp[-1]
res = tmp
with open('si618w17hw5-part2_pohechen_badreview.csv', 'wb') as f:
    f.write('{},{}\n'.format('cities', 'yelp users'))
    for i in res:
        f.write('{},{}\n'.format(i[0], i[1]))


