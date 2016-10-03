#!/usr/bin/python
import sys
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import numpy as np
import pandas as pd
from datetime import datetime,timedelta
import urllib
import calendar
import time

from bokeh.plotting import *
from bokeh.models import HoverTool
from collections import OrderedDict
from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import normalize

interval=10 #First argument is a number of days to look for alerts. 30 default
if len(sys.argv)>1:
    interval=int(sys.argv[1])


import datetime

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        elif isinstance(obj, datetime.date):
            return obj.isoformat()
        elif isinstance(obj, datetime.timedelta):
            return (datetime.datetime.min + obj).time().isoformat()
        else:
            return super(DateTimeEncoder, self).default(obj)


today = datetime.datetime.today()
today = today.replace(second=0, microsecond=0)
query = ('https://data.phila.gov/resource/4t9v-rppq.json?$where=requested_datetime%20between%20%27'+DateTimeEncoder().encode(today-timedelta(days=interval)).strip('"')+'%27%20and%20%27'+DateTimeEncoder().encode(today).strip('"')+'%27')
tdlist = ['expected_datetime','requested_datetime','updated_datetime']

df = pd.read_json(query, convert_dates= tdlist)
df=df.set_index(['service_request_id'])


coord=df[['lat','lon','requested_datetime']].dropna()


coord=coord.reset_index()
ind=np.asarray(coord['service_request_id'])
del coord['service_request_id']

coord=np.asarray(coord)
#coord[:10]

import pyproj as proj

# setup your projections
crs_wgs = proj.Proj(init='epsg:4326') # assuming you're using WGS84 geographic
crs_bng = proj.Proj(init='epsg:26917') # use a locally appropriate projected CRS

# then cast your geographic coordinate pair to the projected system
coord[:,0],coord[:,1]=proj.transform(crs_wgs, crs_bng, coord[:,1], coord[:,0])


coord[:,0] = (coord[:,0] - coord[:,0].min()) / (coord[:,0].max() - coord[:,0].min())
coord[:,1] = (coord[:,1] - coord[:,1].min()) / (coord[:,1].max() - coord[:,1].min())

scl=MinMaxScaler()
coord[:,2]=scl.fit_transform([time.mktime(z.timetuple()) for z in coord[:,2]])

X=coord#[:,:2]
db = DBSCAN(eps=0.004, min_samples=10).fit(X)
core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
labels = db.labels_

# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

print("Clusters found",n_clusters_)

lbls=pd.DataFrame({'nclus':labels},index=ind)
lbls.index.name='service_request_id'

clasf=pd.concat([lbls,df.loc[:,['address', 'agency_responsible', 'expected_datetime', 'requested_datetime',
       'service_name', 'service_notice',
       'updated_datetime','status']]],axis=1)
clasf=clasf[clasf.nclus>=0]
from IPython.display import display, HTML
#for i in range(n_clusters_):
#    display(clasf[clasf.nclus==i])
clasf.sort_values('nclus',inplace=True)

clasf.to_csv('clusters_utf.csv',encoding='utf-8')

import codecs
tstf = codecs.open('clusters_utf.csv', 'r', encoding='ascii', errors='ignore')
tst=pd.read_csv(tstf,index_col='service_request_id')
tst.to_html('clusters.html')
tstf.close()