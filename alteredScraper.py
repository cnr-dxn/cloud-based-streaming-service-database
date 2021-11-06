from bs4 import BeautifulSoup
from sqlite3 import Error
from sqlite3 import connect
from time import sleep
from mysql.connector.constants import ClientFlag
import requests
import os
import sys
import sqlite3
import hashlib
import time
import random
import mysql.connector
from databaseFunctions import insertIfExists
from databaseFunctions import createConnection
from databaseFunctions import findCorrespondingServiceKey
from databaseFunctions import insertLogInstance
from databaseFunctions import returnDictEntryGivenIndex
from databaseFunctions import getMaxServiceVal
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

def processAndPrintWaitTime(waitCounter):
    while waitCounter > 0:
        midWaitCounter = waitCounter
        sleep(1)
        midWaitCounter = midWaitCounter % (24 * 3600) 
        hourTime = midWaitCounter // 3600
        midWaitCounter %= 3600
        minTime = midWaitCounter // 60
        midWaitCounter %= 60
        secTime = midWaitCounter 
        basicLine = str(hourTime) + ' hours, ' + str(minTime) + ' minutes and ' + str(secTime) + ' seconds'
        print('Time until next upload: ', basicLine, '\r', sep='', end="")
        waitCounter = waitCounter - 1
    return

# ----------------------------------------------------

def processService(connection, service, properService, groupLogTime, masterTitleCounter):
    logStartTime = int(time.time())
    titleCounter = 0
    currentDelimiter = 0
    totalSleepTime = 0
    while currentDelimiter < 150000:
        continueProcessing = False
        baseURL = BASE_URL_COMPONENT_1 + service + BASE_URL_COMPONENT_3 + str(currentDelimiter)
        while (1 > 0):
            try:
                content = requests.get(baseURL)
                break
            except:
                print()
                print("FLAGGED: waiting 2 HOURS")
                processAndPrintWaitTime(connection, 7200)
                print()
        soup = BeautifulSoup(content.text, 'html.parser')
        for row in soup.findAll('tr'):
            parts = row.findAll('td')
            if parts is not None and len(parts) > 0:
                continueProcessing = True
                title = parts[1].get_text()
                year = parts[3].get_text()
                ifTv = parts[2].get_text()
                if ifTv != '':
                    ifTv = "Series"
                else:
                    ifTv = "Film"
                insertIfExists(connection, title, year, ifTv, properService)
                titleCounter = titleCounter + 1
                masterTitleCounter = titleCounter
                if (masterTitleCounter - 1) % 2000 == 0 and masterTitleCounter > 1:
                    print()
                    connection.commit()
                    connection.close()
                    processAndPrintWaitTime(40200) 
                    connection = mysql.connector.connect(**config)
                    print()
                boldProperService = "\033[1m" + properService + "\033[0m"
                print('Titles from ', boldProperService, ': ', titleCounter, '\r', sep='', end="")
        if continueProcessing == False:
            grossLogTime = int(int(time.time()) - logStartTime) 
            netLogTime = int(grossLogTime - totalSleepTime)
            streamingKey = findCorrespondingServiceKey(connection, properService)
            insertLogInstance(connection, groupLogTime, streamingKey, titleCounter, netLogTime)
            print()
            return titleCounter
        currentDelimiter = currentDelimiter + 50
        randTime = 0
        totalSleepTime = totalSleepTime + randTime

while 1 > 0:
    print()
    print("========= OVERVIEW =========")
    startTime = time.time()
    connection = mysql.connector.connect(**config)
    entireCounter = 0
    indexCounter = 1
    upperLoopLimit = getMaxServiceVal(connection)
    while (indexCounter <= upperLoopLimit):
        dictEntry = returnDictEntryGivenIndex(connection, indexCounter)
        for i in dictEntry.keys():
            sys.stdout.flush()
            sum = processService(connection, i, dictEntry[i], startTime, entireCounter)
            entireCounter = entireCounter + sum
        indexCounter = indexCounter + 1
        sleep(86400)
    print("- - - - - - - - - - - - - - ")
    print("Total Titles added:", entireCounter)
    endTime = time.time()
    grossTimeDifference = endTime - startTime
    grossMinTime = int(grossTimeDifference / 60)
    grossSecTime = int(grossTimeDifference % 60)
    print("Total time taken:", grossMinTime, "minutes and", grossSecTime, "seconds") 
    print("Time per scan:", float(grossTimeDifference / entireCounter), "seconds")
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
    connection.commit()
    connection.close()
    exit()
