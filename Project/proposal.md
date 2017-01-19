# Project Proposal                                
### Chen, Po-Heng (pohechen)
### Summary and Motivation
As a person dreaming of traveling around the world, living like a local rather than looking around like a tourist when visiting an exotic place is always what I put into practice. Airbnb is a convenient platform where traveler can find a stay in local home. However, most of the time, travelers don't know if the locations they are heading to stay are safe or not. I plan to analyze the relationship between crime types/amount and Airbnb listing data of rating/number of reviews/price to provide a big picture of appropriate location for travelers to stay.

### Dataset Description

The two datasets to be used are: 1. Airbnb activities in Boston dataset uploaded by Airbnb from [Kaggle](https://www.kaggle.com/airbnb/boston) and 2. Boston crime incident report dataset from [City of Boston.gov](https://data.cityofboston.gov/Public-Safety/Crime-Incident-Reports-August-2015-To-Date-Source-/fqn4-4qap).

- Airbnb Dataset: including three sub-datasets, listings.csv, calendar.csv and reviews.csv. I will be focusing on the first two. 
    - listings.csv: It covers comprehensive description of homestay listings from price, location, rating to household facilities. There are 3585 unique listings with 95 features. 
    - calendar.csv: It covers everyday prices of 3585 listings in a full year from 2016-09-06 to 2017-09-05<sup>[*](#1)</sup>. It contains 1308890 rows and 4 columns.
- Boston Crime Dataset: it contains the date, time, offense types, offense description, if shooting occurs, street and exact latitude and longitude. It covers from 2015-08 to now (2017-01). It has 155598 rows and 17 columns.

### Data Manipulation 

The data manipulation will be implemented in R with data.table and dplyr packages. First of all, I will trim listings.csv into simpler data table by removing useless columns such as host_name, host_url, room_type and etc. For Boston crime dataset, I will also remove the date not matching to the one in listings.csv. 

I partition Boston city into 44 smaller units by zip code to cluster Airbnb data and crime data. The Airbnb dataset already has zip code data but Boston crime dataset doesn't. I will use [ZipCodeAPI](https://www.zipcodeapi.com/API) to convert the crime coordinates into zip codes.

The last step will be building a data table with summarized Airbnb data, such as average rating/pricing, and summarized crime data of each zipcode, such as most frequent type/time period/day of week of crime.

### Data Visualization 

The basic built-in plot function and ggplot2 in R both support basic data visualization such as scatter plot, box chart and histogram to check the relationships between interested variables. I plan to do some explanatory data analysis on the relationships of price/rating/number of reviews versus number of crimes, crime types.

For more interesting data visualization, I want to build a dynamic Google map where users can check the Airbnb homestay information and its neighborhood historical crime information at the same time.

<a name="1">*</a> <small>It is not typo. The dataset from Airbnb does say from 2016-09-06 to 2017-09-05. According to my observation, it might be an accident of adding one more year in the date column.</small>