'''
    Author: Luke Putz
    Title: Email Spider
    Date: February 15, 2017
    Description: Crawls a website to find em
    			 stores them in an sqlite3 DB
'''
import os, sys, re, sqlite3, urllib.request, unicodedata
def remove_duplicates(line):
	seen = set()
	result = []
	for item in line:
		if item not in seen:
			seen.add(item)
			result.append(item)
	return result

def create_table(cur):
	cur.execute('''CREATE TABLE IF NOT EXISTS Directory
       (ID INTEGER PRIMARY KEY,
       FIRST TEXT,
       LAST TEXT,
       EMAIL TEXT);''')
	print ("Table created successfully")

def insert(conn, cur, result, first, last):
	for i in range ( len (first) ):
		email = result[i]
		fname = first[i]
		lname = last[i]
		cur.execute('INSERT INTO Directory (ID, FIRST, LAST, EMAIL) VALUES (Null, ?, ?, ?)', (fname, lname, email) )
		conn.commit()

def display(cur):
	for row in cur:
   		print ("ID = ", row[0])
   		print ("FNAME = ", row[1])
   		print ("LNAME = ", row[2])
   		print ("EMAIL = ", row[3], "\n")

def main():
	if len(sys.argv) > 1: 
		with urllib.request.urlopen('https://www.ohio.edu/engineering/about/people/') as ins:
			text = ins.read().decode('utf-8')
			new_emails = re.findall('[a-z0-9\.\-+_]+@ohio.edu', text, re.I)
			text = unicodedata.normalize('NFKD', text) #normalize the text
			names = re.findall('(?:profile=(?:.*">))(.*)\s([a-z].*)(?:<\/a>)', text, re.I)
			first, last = zip(*names) #split the list of tuples
			first = list(first)
			last = list(last)
			#remove duplicates
			result = remove_duplicates(new_emails)
			try:
				conn = sqlite3.connect(sys.argv[1])
				cur = conn.cursor()
				create_table(cur)
				insert(conn, cur, result, first, last)
				cur = conn.execute("SELECT ID, FIRST, LAST, EMAIL  from Directory")
				display(cur)
			except sqlite3.Error as e:
				print("An error occurred:", e.args[0])
	else:
		print('Usage: thisprogram.py database.db')
		print(sys.argv[0])
		exit(1)


if __name__ == '__main__':
    main()
