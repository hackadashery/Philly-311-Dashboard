#!/usr/bin/env python

# make sure to install these packages before running:
# pip install pandas
# pip install bokeh

import numpy as np
import pandas as pd
import datetime
import urllib

from bokeh.plotting import *
from bokeh.models import HoverTool
from collections import OrderedDict

query = ("https://data.phila.gov/resource/4t9v-rppq.json")
raw_data = pd.read_json(query)




