import sqlite3 as sqlite
import pandas as pd


# read in vehicle csv
d = pd.read_csv('vehicles.csv')
# select some columns
d = d[['year', 'make', 'model', 'VClass', 'cylinders', 'displ', 'trany', 'city08', 'highway08', 'comb08']]

# remove "cylinders" is nan
d = d[~d.cylinders.isnull()]
# remove 'displ' is 0
d = d.query('displ != 0')

# connect to database
conn = sqlite.connect('vehicles.db')
# cur = conn.cursor()   
# cur.execute("DROP TABLE IF EXISTS Cars") 
# cur.execute("CREATE TABLE Cars(Year INT, Make TEXT, Model Text, VClass Text, cylinders Float, displ float, trany Text, city08 Int, highway08 Int, comb08 Int)")

# for index, row in d.iterrows():
#     to_insert = "INSERT INTO Cars VALUES({}, '{}', '{}', '{}', {}, {}, '{}', {}, {}, {})".format(*row.tolist())
#     cur.execute(to_insert)

d.to_sql('Cars', conn)
conn.commit()
if conn:
    conn.close()
