import pickle

import petl as etl
import csv

cols = [[0, 1, 2], ['a', 'b','c']]
table1 = etl.fromcolumns(cols)
print(table1)

###########################CSV Reading###############################

table2 = etl.fromcsv('AAPL.csv')

print(table2['Date'])
print(table2)

etl.tocsv(table1, 'example.csv') #wrting to a CSV file


##########################Reading from Pickle files####################

"""" 
what is pickle?
Pickling is a way to convert a python object (list, dict, etc.) into a character stream.
The idea is that this character stream contains all the information necessary to reconstruct
the object in another python script.
"""
#Creating a pickle file

a = ['test value','test value 2','test value 3']

file_Name = "testfile"
# open the file for writing
fileObject = open('pickel_file.p','wb')

# this writes the object a to the
# file named 'testfile'
pickle.dump(a,fileObject)

# here we close the fileObject
fileObject.close()

table3=etl.frompickle('pickel_file.p')
print('Pick')
print(table3)


###################Reading Text Files#################################

text = 'a,1\nb,2\nc,2\n'
with open('example.txt', 'w') as f:
    f.write(text)

table4 = etl.fromtext('example.txt')
print(table4)


################Reading XML files##################################

table5 = etl.fromxml('data.xml', 'tr', 'td')
print(table5)

################Reading JASON files###############################

data = '''
[{"foo": "a", "bar": 1},
{"foo": "b", "bar": 2},
{"foo": "c", "bar": 2}]
'''
with open('example.json', 'w') as f:
    f.write(data)

table6 = etl.fromjson('example.json', header=['foo', 'bar'])
print(table6)

###############Getting data from facebook#######################

#Documentation- https://facebook-sdk.readthedocs.io/en/latest/api.html
import json
import facebook
import re


def main():
    token = "391738|0U8e9WpBWfvBWcdjV7WoJzxjH-s"
    graph = facebook.GraphAPI(token)

    places = graph.search(type='place', center='37.8136, 77.2177',
                          fields='name, location')



    print(json.dumps(places))

    jason_string=str(places['data'])
    data_= re.sub('\'',  '"', jason_string)
    print(data_)
    f = open("facebook_.json", "w")
    f.write(data_)
    f.close()



    table6 = etl.fromjson('facebook_.json', header=['name', 'location'])
    print(table6)

    #for place in places['data']:
      #  print('%s %s' % (place['name'].encode(), place['location'].get('zip')))


if __name__ == '__main__':
    main()


#####################SQL DB Read############################

import sqlite3
connection = sqlite3.connect('sqlite.db')
table7 = etl.fromdb(connection, 'SELECT * FROM demo')
print(table7)

####################EXCEL File Read########################

table8 = etl.fromxls('Financial Sample.xlsx')
print(table8)

###################Get data from wiki####################

#Documentation- https://pypi.org/project/Wikipedia-API/

import wikipediaapi
wiki_wiki = wikipediaapi.Wikipedia('en')

page_py = wiki_wiki.page('Python_(programming_language)')

print(page_py)
print("Page - Summary: %s" % page_py.summary)


####################GoogleAnalytics data##########################


#create a app according to your site using Google anlytics , add the generated code to site, create google api access account.

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = 'googleanalatics_cred.json'
VIEW_ID = '202885465'


def initialize_analyticsreporting():
  """Initializes an Analytics Reporting API V4 service object.

  Returns:
    An authorized Analytics Reporting API V4 service object.
  """
  credentials = ServiceAccountCredentials.from_json_keyfile_name(
      KEY_FILE_LOCATION, SCOPES)

  # Build the service object.
  analytics = build('analyticsreporting', 'v4', credentials=credentials)

  return analytics


def get_report(analytics):
  """Queries the Analytics Reporting API V4.

  Args:
    analytics: An authorized Analytics Reporting API V4 service object.
  Returns:
    The Analytics Reporting API V4 response.
  """
  return analytics.reports().batchGet(
      body={
        'reportRequests': [
        {
          'viewId': VIEW_ID,
          'dateRanges': [{'startDate': '7daysAgo', 'endDate': 'today'}],
          'metrics': [{'expression': 'ga:sessions'}],
          'dimensions': [{'name': 'ga:country'}]
        }]
      }
  ).execute()


def print_response(response):
  """Parses and prints the Analytics Reporting API V4 response.

  Args:
    response: An Analytics Reporting API V4 response.
  """
  for report in response.get('reports', []):
    columnHeader = report.get('columnHeader', {})
    dimensionHeaders = columnHeader.get('dimensions', [])
    metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])

    for row in report.get('data', {}).get('rows', []):
      dimensions = row.get('dimensions', [])
      dateRangeValues = row.get('metrics', [])

      for header, dimension in zip(dimensionHeaders, dimensions):
        print(header + ': ' + dimension)

      for i, values in enumerate(dateRangeValues):
        print ('Date range: ' + str(i))
        for metricHeader, value in zip(metricHeaders, values.get('values')):
          print (metricHeader.get('name') + ': ' + value)


def main():
  analytics = initialize_analyticsreporting()
  response = get_report(analytics)
  print_response(response)

if __name__ == '__main__':
  main()
