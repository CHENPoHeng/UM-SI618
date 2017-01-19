#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Lab 3 (20 points): SQL queries for adding and retrieving database records
# Based on an earlier problem created by Dr. Yuhang Wang

# In this lab you will add the appropriate SQL queries at the marked points
# in this code framework to obtain output that matches the sample desired output.
# There are two XML input files: customer.xml and nation.xml.
# You will first read these files using the provided read_xml_file function
# and create the tables in the database using SQL commands.
# You will then perform various kinds of retrieval operations with SQL on
# the tables you created.

import xml.etree.ElementTree as ET
import sqlite3 as sqlite
import sys

###------- FRAMEWORK CODE: Do not modify the code below
def check_result(result, desired):
  if result != desired:
    print "NOT_OK.  Expected " + desired + "; but got "+result
  else:
    print "OK!"
  return

def read_xml_file(xml_filename, field_types):
  tree = ET.parse(xml_filename)
  root = tree.getroot()
  lot = []
  for child in root:
    fields = []
    for gc in child:
      fields.append(gc.text)

    field_list = []
    count = 0
    for f in fields:
      t = field_types[count]
      if t == 'int':
        field_list.append(int(f))
      elif t == 'string':
        field_list.append(f)
      elif t == 'float':
        field_list.append(float(f))
      else:
        field_list.append(f)
      count = count + 1
      
    lot.append(tuple(field_list))
  return lot;
###------- FRAMEWORK CODE: Do not modify the code above

# The format of the customer.xml file records:
  #<T>
  #  <C_CUSTKEY>1</C_CUSTKEY>
  #  <C_NAME>Customer#000000001</C_NAME>
  #  <C_ADDRESS>IVhzIApeRb ot,c,E</C_ADDRESS>
  #  <C_NATIONKEY>15</C_NATIONKEY>
  #  <C_PHONE>25-989-741-2988</C_PHONE>
  #  <C_ACCTBAL>711.56</C_ACCTBAL>
  #  <C_MKTSEGMENT>BUILDING</C_MKTSEGMENT>
  #  <C_COMMENT>regular, regular platelets are fluffily according to the even attainments. blithely iron</C_COMMENT>
  #</T>
lot = read_xml_file(r'customer.xml',
                    ['int', 'string', 'string', 'int', 'string', 'float', 'string', 'string'])

with sqlite.connect(r'si-601-lab4.db') as con: 
  cur = con.cursor()
  # (1 point) Write a SQL query to erase any existing "customer" table in the database
  cur.execute("DROP TABLE IF EXISTS customer")

  # (1 point) Write a SQL query to create a new "customer" table with the following columns:
  #   C_CUSTKEY (integer)  C_NAME (text)  C_ADDRESS (text)  C_NATIONKEY (integer)  C_PHONE (text)  C_ACCTBAL (real)  C_MKTSEGMENT (text)  C_COMMENT (text)
  cur.execute("CREATE TABLE customer(C_CUSTKEY INT, C_NAME TEXT, C_ADDRESS TEXT, C_NATIONKEY INT, C_PHONE TEXT, C_ACCTBAL REAL, C_MKTSEGMENT TEXT, C_COMMENT TEXT)")

  # (2 points) Write a SQL query to insert the values in the list-of-tuples variable lot into the customer table
  cur.executemany("INSERT INTO customer VALUES(?, ?, ?, ?, ?, ?, ?, ?)", lot)
  con.commit()

  # (2 points) Write a SQL query to compute the count of all records (rows) in the customer table
  cur.execute("SELECT Count(*) FROM customer")
  print "customer count: "
  check_result(str(cur.fetchone()[0]), "1500")

  # (2 points) Write a SQL query to compute the average account balance (C_ACCTBAL) over all rows in the customer table.
  cur.execute("SELECT Avg(C_ACCTBAL) FROM customer")
  print "customer average: "
  check_result(str(cur.fetchone()[0]), "4454.57706")

  # (2 points) Write a SQL query to get the C_CUSTKEY, C_NAME, and C_ACCTBAL columns from the customer table that
  # have C_ACCTBAL >= 1000, and sort the results by C_CUSTKEY
  cur.execute("SELECT C_CUSTKEY, C_NAME, C_ACCTBAL FROM customer WHERE C_ACCTBAL >= 1000 ORDER BY C_CUSTKEY")
  
  # fetchall() method gets all records. It returns a list of tuples.
  # Each of the tuples represent a row in the table.
  rows = cur.fetchall()
  f = open(r'good_customers_desired.txt', 'w')
  f.write('Customer Key' + '\t' + 'Name' + '\t' + 'Account Balance\n')
  for row in rows:
    f.write('\t'.join([str(x) for x in row]) + '\n')
  f.close()

  # (2 points) Write a SQL query to sum the C_ACCTBAL field by market segment C_MKTSEGMENT (call this total column T_ACCTBAL) and sorted by descending T_ACCTBAL
  # Output columns should be C_MKTSEGMENT, and the sum over C_ACCTBAL (sorted by descending amount)
  cur.execute("SELECT C_MKTSEGMENT, sum(C_ACCTBAL) AS T_ACCTBAL FROM customer GROUP BY C_MKTSEGMENT ORDER BY T_ACCTBAL DESC")
  # fetchall() method gets all records. It returns a list of tuples.
  # Each of the tuples represent a row in the table.
  rows = cur.fetchall()
  
  f = open(r'market_segments_summary.txt', 'w')
  f.write('Market Segment' + '\t' + 'Total Customer Account Balance\n')
  for row in rows:
    f.write('\t'.join([str(x) for x in row]) + '\n')
  f.close()

# The format of the nation.xml file records:
  #<T>
  #    <N_NATIONKEY>0</N_NATIONKEY>
  #    <N_NAME>ALGERIA</N_NAME>
  #    <N_REGIONKEY>0</N_REGIONKEY>
  #    <N_COMMENT>final accounts wake quickly. special request</N_COMMENT>
  #</T>

lot = read_xml_file(r'nation.xml', ['int', 'string', 'int', 'string'])

with sqlite.connect(r'si-601-lab4.db') as con: 
  cur = con.cursor()
  # (1 point) Write a SQL query to erase any existing "nation" table in the database
  cur.execute("DROP TABLE IF EXISTS nation")
  
  # (1 point) Write a SQL query to create a new "nation" table with the columns:  N_NATIONKEY (integer)  N_NAME (string)  N_REGIONKEY (integer)  C_COMMENT (text)
  cur.execute("CREATE TABLE nation(N_NATIONKEY INT, N_NAME TEXT,  N_REGIONKEY INT,  C_COMMENT TEXT)")
  
  # (2 points) Write a single SQL query and cursor command here to insert all the tuples into the "nation" table, using the list-of-tuples variable "lot"
  cur.executemany("INSERT INTO nation VALUES(?, ?, ?, ?)", lot)
  con.commit()

  # (4 points) Write a SQL query to compute the total account balance (C_ACCTBAL) in the customer table for each nation.  The output columns
  # should be N_NAME (country name) from the "nation" table and the total account balance, i.e. the sum of C_ACCTBAL in the "customer" table
  # for records grouped by country.  The result should be sorted alphabetically by country name.
  cur.execute('''
    SELECT nation.N_NAME, Sum(customer.C_ACCTBAL) 
    FROM customer JOIN nation ON (customer.C_NATIONKEY == nation.N_NATIONKEY) 
    GROUP BY nation.N_NAME ORDER BY nation.N_NAME''')
  # fetchall() method gets all records. It returns a list of tuples.
  # Each of the tuples represent a row in the table.
  rows = cur.fetchall()
  
  f = open(r'account_balance_by_nation.txt', 'w')
  f.write('Nation Name' + '\t' + 'Total Customer Account Balance\n')
  for row in rows:
    f.write('\t'.join([str(x) for x in row]) + '\n')
  f.close()
    