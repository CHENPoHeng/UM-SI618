# Project Proposal                                
### Chen, Po-Heng (pohechen)
### Summary and Motivation
As a person dreaming of traveling around the world, living like a local rather than looking around like a tourist when visiting an exotic place is always what I put into practice. Airbnb is a convenient platform where traveler can find a stay in local home. However, most of the time, travelers don't know if the locations they are heading to stay are safe or not. 

Despite it is turning more and more commercial that travelers lose intimate contacts with local hosts, it still allows travelers to live locally -- living in local home. Due to my personal favor of Airbnb and data analysis, I am interested in figuring out the following questions. 

// 1. What is the relationship between price and dates? Or what are the strategies local hosts apply to adjust price according to date?
// 2. Why are some local hosts more popular than others? Is because of their location, number of reviews or anything else?
// 3. Could we classify local hosts or travelers into different kinds?

//4. How do we know the authenticity of reviews? 

The goal is to have a general analysis of Airbnb ac

### Dataset Description

The two datasets to be used are: 1. Airbnb activities in Boston dataset uploaded by Airbnb from [Kaggle](https://www.kaggle.com/airbnb/boston) and 2. Boston crime incident report dataset from [City of Boston.gov](https://data.cityofboston.gov/Public-Safety/Crime-Incident-Reports-August-2015-To-Date-Source-/fqn4-4qap).

I will use
- listings.csv: It covers comprehensive description of homestay listings from price, location, rating to household facilities. There are 3585 unique listings with 95 features. 
- calendar.csv: It covers everyday prices of 3585 listings in a full year from 2016-09-06 to 2017-09-05. It contains 1308890 rows and 4 columns.
- reviews.csv: It covers the dates, comments, reviewer ids and listing ids of the reviews which 3585 listings have since 2009. It contains 68275 rows and 6 columns.

### Data Manipulation 

The data manipulation will be implemented in R with data.table and dplyr packages. First of all, I will trim the data table of listings.csv into narrow

The mutual key, **listing_id**, in three datasets facilitates the pairing of listing and calendar

### Data Visualization 

The basic built-in plot function and ggplot2 in R both support basic data visualization such as scatter plot, box chart and histogram to check the relationships between interested variables. I plan to do some explanatory data analysis on the relationships of word count of house descriptions & rating, number of reviews & price or date & price. 

For more interesting data visualization, I will use ggmap package to build a dynamic Google map plot where the users can check the historical price changes by location on map. The price changes will cover from 2016 to 2017 in Boston. I might add in different colors to represent different kinds of homestays, price levels or rating levels. 
