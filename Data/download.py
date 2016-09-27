import requests
import os
import sys
import logging
import pandas as pd
import datetime
import urllib
#import wget

url = 'https://data.phila.gov/api/views/4t9v-rppq/rows.csv?accessType=DOWNLOAD'
logging.basicConfig(level=logging.DEBUG)

query = ("https://data.phila.gov/resource/4t9v-rppq.json")
tdlist = ['expected_datetime','requested_datetime','updated_datetime']

raw_data = pd.read_json(query, convert_dates= tdlist)
raw_data=raw_data.set_index(['service_request_id'])

os.chdir(os.path.dirname(sys.argv[0]))


raw_data.to_pickle('311_Requests.pickle')
#raw_data.to_csv('311_Requests.csv')
#raw_data.to_csv('311_Requests.csv')

r = requests.get(url)
with open("311_Requests.csv", "wb") as code:
    code.write(r.content)
logging.debug("Download completed")