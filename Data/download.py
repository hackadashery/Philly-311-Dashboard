import requests
import os
import sys
import logging

url = 'https://data.phila.gov/api/views/4t9v-rppq/rows.csv?accessType=DOWNLOAD'
logging.basicConfig(level=logging.DEBUG)

os.chdir(os.path.dirname(sys.argv[0]))
r = requests.get(url)
with open("311_Requests.csv", "wb") as code:
    code.write(r.content)
logging.debug("Download completed")