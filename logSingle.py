from mysql.connector.constants import ClientFlag
import mysql.connector

# DEFINES:
BASE_URL_COMPONENT_1 = "https://reelgood.com/source/"
BASE_URL_COMPONENT_3 = "?filter-sort=4&offset="
config = {
    'user': 'root',
    'password': 'neal2master@#@',
    'host': '35.239.147.239',
    'client_flags': [ClientFlag.SSL],
    'ssl_ca': 'ssl/server-ca.pem',
    'ssl_cert': 'ssl/client-cert.pem',
    'ssl_key': 'ssl/client-key.pem'
}

def insertSingle(connection, passedTitle, passedYear, rottenScore, inputScore, notes):
    currentCursor = connection.cursor()
    currentCursor.execute("USE mainMedia")
    try:
        currentCursor.execute("INSERT INTO WatchedHistory (whDate, whTitle, whYear, whRottenScore, whMyScore, whNotes) values (CURDATE(), %s, %s, %s, %s, %s)",
            (passedTitle, passedYear, rottenScore, inputScore, notes))
        print("Successfully uploaded ")
        #print()
    except:
        print("selectSpecific: unsuccessful")
        print()
        connection.close()
        exit()
# --------------------------------------------------------------------------------------------------

connection = mysql.connector.connect(**config)
title = input("Enter a title for the log: ")
year = int(input("Enter a year: "))
while year < 1940 or year > 2021:
	year = int(input("Enter a valid year: "))
rtScore = int(input("Enter the Rotten Tomatoes score: "))
while rtScore < 0 or rtScore > 100:
	rtScore = int(input("Enter a valid Rotten Tomatoes Score: "))
myScore = int(input("Enter your personal score: "))
while myScore < 0 or myScore > 100:
	myScore = int(input("Enter a valid Rotten Tomatoes Score: "))
myNotes = input("Enter any notes you had: ")
print("Review: ")
print(" - Title:", title)
print(" - Year:", year)
print(" - Rotten Score:", rtScore)
print(" - Your Score:", myScore)
print(" - Notes:", myNotes)
print("- - - - - - - - - - -")
choice = input(("Submit? (y/n): "))
if choice != 'y':
	pass
else:
	insertSingle(connection, title, year, rtScore, myScore, myNotes)
connection.commit()
connection.close()

