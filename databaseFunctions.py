from time import sleep
import sqlite3
from sqlite3 import Error
from sqlite3 import connect
import hashlib
import time

def createConnection(dbFilename):
    connection = None
    try:
        connection = sqlite3.connect(dbFilename)
    except Error as e:
        print(e)
    return connection

# Junction field: ----------------------------------------------------------------------------------
def findCorrespondingServiceKey(connection, passedServiceName):
    currentCursor = connection.cursor()
    currentCursor.execute("USE mainMedia")
    #query = "SELECT serviceKey FROM ServiceDimension WHERE serviceName = \'" + passedServiceName + "\'"
    #print(query)
    try:
        #currentCursor.execute(query)
        currentCursor.execute("SELECT serviceKey FROM ServiceDimension WHERE serviceName = %s", (passedServiceName,))
        #print("findCorrespondingServiceKey: successful")
    except:
        print("findCorrespondingServiceKey: unsuccessful")
        connection.close()
        exit()
        return
    firstResult = currentCursor.fetchall()
    #print(firstResult)
    result = [i[0] for i in firstResult]
    return result[0]

def findCorrespondingMediaKey(connection, passedMediaHash):
    currentCursor = connection.cursor()
    currentCursor.execute("USE mainMedia")
    #query = "SELECT mediaKey FROM MediaDimension WHERE mediaHash = \'" + passedMediaHash + "\'"
    try:
        #currentCursor.execute(query)
        currentCursor.execute("SELECT mediaKey FROM MediaDimension WHERE mediaHash = %s", (passedMediaHash,))
        #print("findCorrespondingMediakey: successful")
        #print()
    except:
        print("findCorrespondingMediakey: unsuccessful")
        print()
        connection.close()
        exit()
        return
    firstResult = currentCursor.fetchall()
    result = [i[0] for i in firstResult]
    return result[0]

def insertInstance(connection, passedMediaKey, passedServiceName):
    currentCursor = connection.cursor()
    currentCursor.execute("USE mainMedia")
    passedServiceKey = findCorrespondingServiceKey(connection, passedServiceName)
    #print("passedMediaKey:", passedMediaKey)
    #print("passedServiceKey:", passedServiceKey)
    #print("int(time.time()):", int(time.time()))
    #print()
    currTime = int(time.time())
    try:
        currentCursor.execute("INSERT INTO MediaServiceFact (MSmediaKey, MSserviceKey, msTimeStamp) VALUES (%s, %s, %s)",
                (passedMediaKey, passedServiceKey, currTime))
        #print("insertInstance: successful")
        #print()
    except:
        print("insertInstance: unsuccessful")
        connection.close()
        exit()
# --------------------------------------------------------------------------------------------------

# LogHistoryField ----------------------------------------------------------------------------------
def insertLogInstance(connection, timeAtLog, serviceKey, quantityLogged, totalLogTime):
    pass
    currentCursor = connection.cursor()
    currentCursor.execute("USE mainMedia")
    totalLogInt = int(totalLogTime)
    timeAtLogInt = int(timeAtLog)
    try:
        currentCursor.execute("INSERT INTO LogHistory (logHistoryTimeTaken, logHistoryTimeAtLog, logHistoryQuantity, logHistoryStreamingKey) VALUES (%s, %s, %s, %s)",
                (totalLogInt, timeAtLogInt, quantityLogged, serviceKey))
        #print("insertLogInstance: successful")
        #print()
    except:
        print("insertLogInstance: unsuccessful")
        connection.close()
        exit()
        return
# --------------------------------------------------------------------------------------------------

# MediaDimension field: --------------------------------------------------------------------------
def returnMD5Hash(str1, str2, str3):
    firstHalf = str(len(str1))+"#"+str1
    firstComp = hashlib.md5(firstHalf.encode()).hexdigest()
    secondHalf = str(str2)+"#"+str(str2)
    secondComp = hashlib.md5(secondHalf.encode()).hexdigest()
    thirdHalf = str(len(str3))+"#"+str3
    thirdComp = hashlib.md5(thirdHalf.encode()).hexdigest()
    final = hashlib.md5((firstComp+secondComp+thirdComp).encode()).hexdigest()
    return final

def insertIfExistsHelper(connection, currHash):
    currentCursor = connection.cursor()
    currentCursor.execute("USE mainMedia")
    try:
        currentCursor.execute("SELECT * FROM MediaDimension WHERE mediaHash = %s", (currHash,))
        #print("insertIfExistsHelper: successful")
        #print()
    except:
        #print("insertIfExistsHelper: unsuccessful")
        #print()
        connection.close()
        exit()
    rows = currentCursor.fetchall()
    if len(rows) != 0:
        #print("insertIfExistsHelper returning false")
        #print()
        return False
    else:
        #print("insertIfExistsHelper returning true")
        #print()
        return True

def insertIfExists(connection, mediaTitle, mediaYear, mediaType, serviceName):
    #print()
    currentCursor = connection.cursor()
    currentCursor.execute("USE mainMedia")
    currentHash = returnMD5Hash(mediaTitle, mediaYear, mediaType)
    if insertIfExistsHelper(connection, currentHash) == True:
        try:
            currentCursor.execute("INSERT INTO MediaDimension (mediaTitle, mediaYear, mediaType, mediaHash) values (%s, %s, %s, %s)",
                (mediaTitle, mediaYear, mediaType, currentHash))
            #print("insertIfExists: successful")
            #print()
        except:
            print("insertIfExists: unsuccessful")
            print()
            connection.close()
            exit()
            return
    insertInstance(connection, findCorrespondingMediaKey(connection, currentHash), serviceName)
    
# --------------------------------------------------------------------------------------------------

# ALL field: ---------------------------------------------------------------------------------------
def selectAll(connection, tableName):
    currentCursor = connection.cursor()
    currentCursor.execute("USE mainMedia")
    query = "SELECT * FROM " + tableName
    try:
        currentCursor.execute(query)
        # print("selectAll: successful")
    except:
        # print("selectAll: unsuccessful")
        connection.close()
        exit()
    rows = currentCursor.fetchall()
    for i in rows:
        print(i)

def descriptTableAll(connection, tableName):
    currentCursor = connection.cursor()
    currentCursor.execute("USE mainMedia")
    query = "SELECT * FROM " + tableName
    try:
        currentCursor.execute(query)
        # print("descriptTable: success")
    except:
        # print("descriptTable: unsuccessful")
        connection.close()
        exit()
        return
    names = list(map(lambda x: x[0], currentCursor.description))
    print(names)

def selectSpecific(connection, titleName):
    currentCursor = connection.cursor()
    currentCursor.execute("USE mainMedia")
    try:
        currentCursor.execute("SELECT MediaDimension.mediaTitle, ServiceDimension.serviceName, MediaDimension.mediaType, MediaDimension.mediaYear FROM MediaDimension, ServiceDimension, MediaServiceFact WHERE MediaDimension.mediaKey = MediaServiceFact.MSmediaKey AND ServiceDimension.serviceKey = MediaServiceFact.MSserviceKey AND UNIX_TIMESTAMP(NOW()) - MediaServiceFact.MSTimeStamp < 604800 AND MediaDimension.mediaTitle LIKE Concat('%', %s,'%') ORDER BY MediaDimension.mediaYear DESC", (titleName,))
        #print("selectSpecific: successful")
        #print()
    except:
        print("selectSpecific: unsuccessful")
        print()
        connection.close()
        exit()
    rows = currentCursor.fetchall()
    if len(rows) == 0:
        print("No results found for \"", titleName, "\"", sep='')
        return
    print()
    seperator = "\033[1m" + "|" + "\033[0m"
    print("Results: ")
    for i in rows:
        shortCounter = 0
        for j in i:
            if shortCounter == len(i) - 1:
                print(j)
            else:
                print(j,seperator, end=' ')
            shortCounter = shortCounter + 1
# --------------------------------------------------------------------------------------------------

# Service Field: -----------------------------------------------------------------------------------
def returnDictEntryGivenIndex(connection, index):
    currentCursor = connection.cursor()
    currentCursor.execute("USE mainMedia")
    # function: access specific row of database, take url and name out of row, put into dictionary
    # - idiot, just use serviceKey as the thing
    # - 
    try: 
        currentCursor.execute("SELECT serviceURLTitle, serviceName FROM ServiceDimension WHERE serviceKey = %s", (index,))
        #print("returnDictGivenIndex: successful")
    except:
        print("returnDictGivenIndex: unsuccessful")
        print()
    rows = currentCursor.fetchall()
    url = str(rows[0][0])
    name = str(rows[0][1])
    returnDictEntry = { url: name }
    return returnDictEntry

def getMaxServiceVal(connection):
    currentCursor = connection.cursor()
    currentCursor.execute("USE mainMedia")
    try:
        currentCursor.execute("SELECT serviceKey FROM ServiceDimension ORDER BY serviceKey DESC LIMIT 1")
        #print("getMaxServiceVal: successful")
        #print()
    except:
        #print("getMaxServiceVal: unsuccessful")
        #print()
        connection.close()
        exit()
    rows = currentCursor.fetchall()
    maxInt = rows[0][0]
    return (int(maxInt))
# --------------------------------------------------------------------------------------------------

# Testing Field: -----------------------------------------------------------------------------------
#conn = createConnection('finalTest.db')
#descriptTable(conn, "MediaDimension")
#descriptTable(conn, "MediaServiceFact")
#descriptTable(conn, "ServiceDimension")
#print("Before changes: --------------------------")
#selectAll(conn, "MediaDimension")
#print(" - - - - - - - ")
#selectAll(conn, "MediaServicefact")
#print("------------------------------------------")
#insertIfExists(conn, "The Social Network", 2011, "Film", "Peacock")
#print("After changes: ---------------------------")
#selectAll(conn, "MediaDimension")
#print(" - - - - - - - ")
#selectAll(conn, "MediaServicefact")
#print("------------------------------------------")
#conn.commit()
#conn.close()
