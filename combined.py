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

connection = mysql.connector.connect(**config)
name = input("Please enter a title to be found: ")
selectSpecific(connection, name)
connection.close()

