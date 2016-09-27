import requests
import os
import sys
import logging
import pandas as pd
import datetime
import urllib

#url = 'https://data.phila.gov/api/views/4t9v-rppq/rows.csv?accessType=DOWNLOAD'
logging.basicConfig(level=logging.DEBUG)

query = ("https://data.phila.gov/resource/4t9v-rppq.json")
tdlist = ['expected_datetime','requested_datetime','updated_datetime']

raw_data = pd.read_json(query, convert_dates= tdlist)

os.chdir(os.path.dirname(sys.argv[0]))

raw_data.to_csv('311_Requests.csv')

# r = requests.get(url)
# with open("311_Requests.csv", "wb") as code:
#     code.write(r.content)
logging.debug("Download completed")