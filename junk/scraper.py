# pylint: disable=fixme, line-too-long
from bs4 import BeautifulSoup
import requests
import os
import sys
from time import sleep
import sqlite3
from sqlite3 import Error
from sqlite3 import connect
import hashlib
# DEFINES:
# ----------------------------------------------------
PASSED_SERVICES = {"disney_plus" : "Disney+", 
                  "netflix" : "Netflix", 
                  "peacock" : "Peacock", 
                  "hulu" : "Hulu", 
                  "amazon" : "Amazon Prime Video", 
                  "hbo_max" : "HBO Max"}
BASE_URL_COMPONENT_1 = "https://reelgood.com/source/"
BASE_URL_COMPONENT_3 = "?filter-sort=4&offset="
# ----------------------------------------------------

def processService(service):
    print("Loading... ")
    titleCounter = 0
    filetool = open("output.txt", "a")
    currentDelimiter = 0
    while currentDelimiter < 150000:
        determiner = False
        baseURL = BASE_URL_COMPONENT_1 + service + BASE_URL_COMPONENT_3 + str(currentDelimiter)
        content = requests.get(baseURL)
        soup = BeautifulSoup(content.text, 'html.parser')
        for row in soup.findAll('tr'):
            parts = row.findAll('td')
            if parts is not None and len(parts) > 0:
                determiner = True
                title = parts[1].get_text()
                ifTv = parts[2].get_text()
                year = parts[3].get_text()
                line = title + " | " + PASSED_SERVICES[service] + " | "
                if ifTv != '':
                    line = line + "Series | "
                else:
                    line = line + "Film | "
                line = line + year
                filetool.write(line)
                filetool.write("\n")
                titleCounter = titleCounter + 1
                sleep(0.002)
                print('Titles: ', titleCounter, '\r', sep='', end="")
        if determiner == False:
            break
        currentDelimiter = currentDelimiter + 50
    return titleCounter

#os.remove("output.txt")
for i in PASSED_SERVICES.keys():
    print("examining:", PASSED_SERVICES[i], "\r")
    sys.stdout.flush()
    sum = processService(i)
    print("wrote", sum, "files to file from", PASSED_SERVICES[i])