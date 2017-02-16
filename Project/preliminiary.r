library(data.table)
library(dplyr)
library(ggplot2) # learn ggplot2 T_T
options(digits=22)
len = length
## load in data 
# read in crime data
c = read.csv('bostonCrime.csv')
ac = read.csv('airbnbCalendar.csv', as.is = T) # airbnb calendar
ac$price = as.numeric(gsub('\\$|\\,', '', ac$price))
ac = as.data.table(ac)
al = read.csv('airbnbListings.csv', as.is = T) # airbnb listing

# rename 
names(c) = c('incident.id', 'offense.code', 'offense.group', 'offense.dis',
             'dist', 'report.area', 'shooting', 'date', 'hr', 'yr', 'mon',
             'day', 'ucr', 'street', 'lat', 'long', 'loc')
# remove unlocated data
i = which(c$long == -1 | is.na(c$long))
if(len(i)) c = c[-i, ]

# remove useless column
i = which(names(al) %in% c('listing_url', 'scrape_id', 'last_scraped', 'experiences_offered',
          'thumbnail_url', 'medium_url', 'picture_url','xl_picture_url','host_url',
          'host_thumbnail_url', 'host_picture_url','jurisdiction_names','license',
          'requires_license', 'calendar_last_scraped', 'has_availability', 'calendar_updated',
          'state'))
if(len(i)) al = al[, -i]
al = data.table(al)
ac = unique(ac)

## take a look of crime data
## time
# crime occurance time
ggplot(c, aes(hr)) + 
    geom_histogram(binwidth  = 1, col = 'black', fill = 'lightblue')

ggplot(c, aes(mon)) + 
    geom_histogram(binwidth  = 1, col = 'black', fill = 'lightblue')
# perhaps the data starts from Aug '15 to Jan '17

# percentage of shooting 
table(c$shooting)[2] / nrow(c) * 100

# crime categories 
unique(c$offense.group)
table(c$offense.group) # make a list

tmp = c %>% group_by(offense.group) %>% summarize(p = n()/nrow(c) * 100) 
tmp = tmp[with(tmp, order(-p)), ]
ggplot(as.data.frame(tmp), aes(x = offense.group, y = p)) +
    geom_bar(position="dodge",stat="identity") + 
    coord_flip() 

## airbnb 
# identify_verified percentage
tmp = al %>% group_by(host_identity_verified) %>% summarize(p = n()/nrow(al)) %>% rename(hid = host_identity_verified)
ggplot(melt(tmp), aes(x = variable, y=  value,fill = value)) + 
    geom_bar(position = "fill",stat = "identity") + 
    scale_y_continuous(labels = percent_format())

##### build airbnb and crime data
# use ggmap to convert all long, lat into zip
m = read.csv('isd_neighborhood_districts.csv', as.is = T)

res = list()
for(j in 1:len(m$Name)) {
    x = gsub('\\(|\\)', '', m$the_geom[j])
    x = strsplit(x, " |,")[[1]]
    x = as.data.frame(matrix(unlist(x), ncol = 3, byrow = T), stringsAsFactors = F)
    x$V1 = NULL
    x = sapply(x, as.numeric)
    res[[m$Name[j]]] = x
}

# allocate crime points into each counties
library(SDMTools)
clist = list()
ctmp = c[, c('long', 'lat')]
c$county = NA
for(n in m$Name){
    poly = res[[n]]
    tmp = pnt.in.poly(ctmp[,c("long","lat")], poly)
    i = which(tmp$pip != 0)
    c[i, ]$county = n
}

# allocate airbnb member into region
al$county = NA
atmp = al[, c('id', 'longitude', 'latitude')]
for(n in m$Name) {
    poly = res[[n]]
    tmp = pnt.in.poly(atmp[, c('longitude', 'latitude')], poly)
    i = which(tmp$pip != 0)
    if(len(i)) al[i, ]$county = n
}


# see crime distribution
al = al[-which(is.na(al$county)),]
plot(al$longitude, al$latitude, col = 'blue', pch = '.')
points(c$long, c$lat, col = 'red', pch = '.')
plot(x$longitude, x$latitude, pch = '.')
for(i in 1:len(m$Name)) {
    points(res[[i]], pch = '.', type = 'l', col = 'black')
}
i = which(is.na(al$county))
plot(al[i, ]$longitude, al[i, ]$latitude, pch = '.')

for(i in c(0,1)){
    points(tmp[which(tmp$pip == i), c('longitude', 'latitude')], col = 1 + i)
}

## create a county-based dataframe
# crime 
c.summary = c %>% group_by(county, offense.group) %>% summarize(count = n())
# airbnb listing
i = which(ac$available != 'f')
ac = ac[i, ]
ac = ac %>% group_by(listing_id) %>% 
    summarize(p.mean = mean(price), p.med = median(price), p.max = max(price),
              p.min = min(price), p.q25 = quantile(price, .25),
              p.q75 = quantile(price, .75), p.sd = sd(price))
