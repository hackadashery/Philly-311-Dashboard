import requests
import os

url = 'https://data.phila.gov/api/views/4t9v-rppq/rows.csv?accessType=DOWNLOAD'

r = requests.get(url)
f = os.path.join('Data', '311_Requests.csv')
with open(f, "wb") as code:
    code.write(r.content)