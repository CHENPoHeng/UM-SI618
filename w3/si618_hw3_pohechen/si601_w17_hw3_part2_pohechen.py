import sys
import sqlite3 as sql

## take command line argument first
genre = str(sys.argv[1])
num = sys.argv[2]

## connect to database
with sql.connect(r'si618-hw3.db') as con: 
    c = con.cursor()

## a check
c.execute('SELECT DISTINCT genre FROM movie_genre')
tmp = c.fetchall()
tmp = [i[0] for i in tmp]
if genre not in tmp:
    print 'Plz select one kind of genres from the following options:' 
    for i in tmp:
        print i
    sys.exit()


## SQL to extract what user needs
command = '''SELECT movie_actor.actors, count(*) as movie
    FROM movie_actor JOIN movie_genre ON (movie_actor.imdb_id == movie_genre.imdb_id)
    WHERE movie_genre.genre == "''' +  genre  + '''"
    GROUP BY movie_actor.actors
    ORDER BY movie DESC 
    LIMIT ''' + str(num)


c.execute(command)
tmp = c.fetchall()

print 'Top '+ str(num) + ' actors who played in most ' + genre + ' movies:'
print 'Actor, '+ genre +' Movies Played in'
for i, j in tmp:
    print i + ', ' + str(j)