import json

# data are downloaded from 
# https://umich.box.com/s/1lc3o4ib3mgybo86r04ginn90rm0pukx

# read in line by line and append it to a new list
lines = []
for line in open('yelp_academic_dataset.json', 'r'):    
    lines.append(json.loads(line))

# check if each line has 'categories' item
l = [i for i in lines if 'categories' in i]

with open('businessdata.tsv', 'w') as writer:
    header = '\t'.join(['name','city','state','stars','review_count', 'main_category']) + '\n'
    writer.write(header)
    for i in l:
        name = i['name']
        city = i['city']
        state = i['state']
        stars = i['stars']
        review_count = i['review_count']
        if len(i['categories']) == 0:
            main_category = 'NA'
        else:
            main_category = i['categories'][0]
        row = '\t'.join([name, city, state, str(stars), str(review_count), main_category]).encode('utf-8') + '\n'
        writer.write(row)

        