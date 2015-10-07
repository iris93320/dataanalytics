import sqlite3 as lite
import sys
import os 
import csv
import urllib
import re

ratingsList = "http://boxnumbertwo.com/MovieData/ratings.list"
response = urllib.urlopen(ratingsList)

count = 0
currentname = ''
currentvote = 0
currentrate = 0
currentyear = 0
## Set directory to computer
directoryForDB = "/Users/iriszhanfu/Documents/programming M/ "
if not os.path.exists(directoryForDB):
	os.makedirs(directoryForDB)

directoryForDB = directoryForDB + "movies.db"
## If database does not exist, creates items
## If database does exist, opens it
con = lite.connect(directoryForDB)
with con:
	ratingdb = con.cursor()
	ratingdb.execute("DROP TABLE IF EXISTS MoviesInfo") 
	ratingdb.execute("CREATE TABLE MoviesInfo(name TEXT, rate REAL, vote INT, year TEXT, PB INT, DG INT, WG INT)")
	count = 0
	for line in response: #  Get vote, rate, name and year of movies
	   words = re.sub(' +',' ',line.strip()) #  This is a string!
	   save = words.split(" ",3) #  Split vote, rate, name and year
	   vote = int(save[1].replace("'", "")) #  Get votes
	   rate = float(save[2].replace("'", "")) #  Get rates
	   nameANDdate = save[3].split(" (",1) #  Only part of  names have quotation, so we can not split name with quotation
	   name = nameANDdate[0].replace('"', '') #  Get names
	   print name
	   year = nameANDdate[1].replace("?","0") #  Get years, one movie's year is ???? instead of numbers
	   year = re.sub("\D","",year) #  Keep numbers only
	   year = int(year[0:4]) #  Keep the first four year number
	   print year
	   
	   print count
	   if (count==0):
	       currentname = name
	       currentvote = vote
	       currentrate = rate
	       currentyear = year
	   elif name == currentname:
	       if vote>currentvote:
	           currentvote = vote
	           currentrate = rate
	           currentyear = year
	   elif name != currentname:
	       insertStatement = 'INSERT INTO MoviesInfo(name, rate, vote, year) VALUES("%s",%f,%d,%d)' % (currentname,currentrate,currentvote,currentyear) #  Add movies' names and ratings into database
	       ratingdb.execute(insertStatement)
	       currentname = name
	       currentrate = rate
	       currentvote = vote
	       currentyear = year
           
	   count = count +1    
	   #if count>100: #  Limit number
	     #  break
	   
	   
	   
	   #insertStatement = 'DELETE FROM MoviesInfo WHERE vote < (SELECT max(vote) FROM MoviesInfo WHERE name LIKE "%s")' % (name) #  Delete duplicate and keep movie with max vote
	   #ratingdb.execute(insertStatement)		
	## NEEDED, if not, database does not update
	con.commit()
