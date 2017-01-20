# -*- coding: utf-8 -*-

import json
import sqlite3 as sql

with open('movie_actors_data.txt', 'r') as f:
    json_str = f.read()

t_genre = []
t_movie = []
t_actor = []
for i in json_str.split('\n')[:-1]:
    tmp = json.loads(i)

    # parse movie title & genres
    if 'genres' in tmp:
        for j in tmp['genres']:
            t_genre.append(tuple([tmp['imdb_id'], j]))

    # parse movie meta data
    t_movie.append(tuple([tmp['imdb_id'], tmp['title'], tmp['year'], tmp['rating']]))

    # parse movie actor
    if 'actors' in tmp:
        for j in tmp['actors']:
            t_actor.append(tuple([tmp['imdb_id'], j]))


with sql.connect(r'si618-hw3.db') as con: 
    c = con.cursor()

# create SQL movie_genre data table
c.execute("DROP TABLE IF EXISTS movie_genre")
c.execute('''
    CREATE TABLE movie_genre(imdb_id INT, genre TEXT)''')
c.executemany("INSERT INTO movie_genre VALUES(?, ?)", t_genre)

# create SQL movies data table
c.execute("DROP TABLE IF EXISTS movies")
c.execute('''
    CREATE TABLE movies(imdb_id INT, title TEXT, year INT, rating REAL)''')
c.executemany("INSERT INTO movies VALUES(?, ?, ?, ?)", t_movie)

# create SQL movie_actor data table
c.execute("DROP TABLE IF EXISTS movie_actor")
c.execute('''
    CREATE TABLE movie_actor(imdb_id INT, actors TEXT)''')
c.executemany("INSERT INTO movie_actor VALUES(?, ?)", t_actor)

# save them
con.commit()

c.execute("SELECT * FROM movie_genre")
tmp = c.fetchall()



# print out top 10 genres with most movies
c.execute('''SELECT movie_genre.genre, count(*) as movie
    FROM movie_genre JOIN movies ON (movie_genre.imdb_id == movies.imdb_id)
    GROUP BY movie_genre.genre ORDER BY movie DESC LIMIT 10''')
tmp = c.fetchall()
print 'Genre, Movies'
for i, j in tmp:
    print i + ', ' + str(j)

# print out number of movies broken down by year in chronological order 
c.execute('''SELECT year, count(*) as movie
    FROM movies GROUP BY year ORDER BY year ''')
tmp = c.fetchall()
print 'Year, Movies'
for i, j in tmp:
    print str(i) + ', ' + str(j)


# print all Sci-Fi movies order by decreasing rating,
# then by decreasing year if ratings are the same
c.execute('''SELECT movies.title, movies.year, movies.rating
    FROM movies JOIN movie_genre ON (movie_genre.imdb_id == movies.imdb_id)
    WHERE movie_genre.genre == 'Sci-Fi'
    ORDER BY movies.rating DESC, movies.year DESC''')
tmp = c.fetchall()
print 'Title, Year, Rating'
for x, y, z in tmp:
    print x + ', ' + str(y) + ', ' + str(z)

# print an SQL query to find the top 10 actors 
# who played in most movies in and after year 2000.
# In case of ties, sort the rows by actor name.  
c.execute('''SELECT movie_actor.actors, count(*) as movies
    FROM movies JOIN movie_actor ON (movies.imdb_id == movie_actor.imdb_id)
    WHERE movies.year >= 2000
    GROUP BY movie_actor.actors
    ORDER BY movies DESC LIMIT 10''')
tmp = c.fetchall()
print 'Actor, Movies'
for i, j in tmp:
    print i + ', ' + str(j)

# finding pairs of actors who co-stared in 3 or more movies.
# The pairs of names must be unique.
# This means that ‘actor A, actor B’ and ‘actor B, actor A’ 
# are the same pair, so only one of them should appear.
c.execute('''SELECT *
    FROM (
        SELECT a1.actors, a2.actors, count(*) as count
        FROM movie_actor AS a1 JOIN movie_actor AS a2 
        ON (a1.imdb_id == a2.imdb_id and a1.actors < a2.actors)
        GROUP BY a1.actors, a2.actors
        ) AS TMP
    WHERE count >= 3  
    ORDER BY count DESC, TMP.actors 
    ''')
## dont know why cannot put WHERE in the same line
## how do I know the name of new column names of new datatable??
tmp = c.fetchall()
print 'Actor A, Actor B, Co-stared Movies'
for x,y,z in tmp:
    print x + ', ' + y + ', ' + str(z)

###################################################
### reference: 
### group_by multi-criteria:
###     http://stackoverflow.com/questions/2421388/using-group-by-on-multiple-columns
### find all possible combination in a single column:
###     http://stackoverflow.com/questions/31070337/return-all-possible-combinations-of-values-within-a-single-column-in-sql
###################################################