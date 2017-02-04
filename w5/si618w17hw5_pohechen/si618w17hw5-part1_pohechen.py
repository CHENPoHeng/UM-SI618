## My Spark first practice with pyspark
# pyspark is only an API connection to interact with Spark
# -------------------------------------------------------- #
# imports
import re
from pyspark import SparkContext, SparkConf
import json # for yelp json file

## module constant
APP_NAME = 'YelpSummary'

def convert_dict_to_tuples(d):
    city = d['city']
    n_review = d['review_count']
    if d['stars'] >= 4:
        four_star = 1
    else:
        four_star = 0
    tuples = []
    if len(d['neighborhoods']) == 0:
        # neighbor = 'Unknown'
        tuples.append((city, 'Unknown', 1, n_review, four_star))
    else:
        for i in d['neighborhoods']:
            tuples.append((city, i, 1, n_review, four_star))
    return tuples
    

## main functionality
def main(sc):
    f = sc.textFile("hdfs:///var/si618w17/yelp_academic_dataset_business_updated.json")

    # convert each json review into a dictionary
    f = f.map(lambda x : json.loads(x)) 

    # convert a review's dictionary into a list of (city, neighbor, 1, n_review, four_star) tuples
    f = f.flatMap(lambda x : convert_dict_to_tuples(x)) 

    # separately count all features by multiple keys of (city, neighbor)
    f_nB = f.map(lambda x: ((x[0], x[1]), x[2])).reduceByKey(lambda a, b: a + b)
    f_nR = f.map(lambda x: ((x[0], x[1]), x[3])).reduceByKey(lambda a, b: a + b)
    f_nF = f.map(lambda x: ((x[0], x[1]), x[4])).reduceByKey(lambda a, b: a + b)

    # combine them all together by multiple keys of (city, neighbor)
    tmp = f_nB.fullOuterJoin(f_nR)
    tmp = tmp.fullOuterJoin(f_nF)
    tmp = tmp.map(lambda x : (x[0][0],x[0][1],x[1][0][0], x[1][0][1], x[1][1]))    

    # sorted the city alphabetically and then decreasingly sorted by number of business
    res = tmp.sortBy(lambda x: (x[0], -x[2]), ascending = True).collect()

    with open('si618w17hw5-part1_pohechen.tsv', 'wb') as f:
        for i in res:
            f.write('{}\t{}\t{}\t{}\t{}\n'.format(i[0].encode('utf-8'), i[1].encode('utf-8'), i[2], i[3], i[4]))

if __name__ == '__main__':    
    # configure Spark
    conf = SparkConf().setAppName(APP_NAME)
    sc = SparkContext(conf = conf)

    # execute main functionality
    main(sc)


#afterwards on the login node, do:
#hdfs dfs -get spark_wordcount_output spark_wordcount_output
#hdfs dfs -get spark_wordcount_output2 spark_wordcount_output2
#you should have both the folders in your home directory now
#if you will rerun the code, don't forget to first remove the old output
#hdfs dfs -rm -r spark_wordcount_output
#hdfs dfs -rm -r spark_wordcount_output2

