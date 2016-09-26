import requests
import os

url = 'https://data.phila.gov/api/views/4t9v-rppq/rows.csv?accessType=DOWNLOAD'

r = requests.get(url)
with open("311_Requests.csv", "wb") as code:
    code.write(r.content)