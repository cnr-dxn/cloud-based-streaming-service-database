# Cloud-Based Streaming Media Search Framework

A back-end framework for an application that allows for a user to input which streaming services they have access to, and a specific title, and returns all media (films and series) both matching that title and available for them to stream. Made with Python, and backed with a Google Cloud MySQL database, this application was designed to allow for upward scaling, with little to no impact on efficiency, as well as data safety durability. 

**Web Scraping**: In order to allow for authentic and accurate results to be returned, a web-scraping algorithm had to be built-in. This algorithm consists of a series of cURL and data manipulations to take values and from the scraped website to then be stored in the database. This algorithm was designed to be triggered at will, as to not trip the bot scanners from the websites. 

**Database Backed**: The data scraped is then is stored in a relational SQL database, to allow for upward scaling with little to no impact on efficiency. Certain tables were also created to do routine quality checks whenever a query is implemented, and to notify me whenever unexpected return times/values occur. 

**Efficiency and Performance Logging**: The database includes fields that allow me to review the efficiency of inserts and queries within the database, and see exactly where and how I can improve the algorithms within. 

## How to run this application:

This is run as a python3 application, and thus to run, a current version of Python3 version must be running on the system. If so, the following command will run a current search and refresh on the current database:
```
python3 alteredScraper.py
```
The following command (used as a test for the framework) will prompt the user to enter a title to be found, and will print the results found:
```
./combined.py
```
*EDIT: This database became too expensive to maintain and therefore had to be shut down. However, this framework will be connected to the database for **WhatToKnowBeforeWatching.com**, and thus will be used for a feature there*

## File Structure

**alteredScraper.py** updates the database with new titles found at that time

**combined.py** provides a test to examine the results of the framework's update (by providing a simple interface for the user to use)

## Notes

This database became too expensive to maintain and therefore had to be shut down. However, this framework will be connected to the database for **WhatToKnowBeforeWatching.com**, and thus will be used for a feature there
