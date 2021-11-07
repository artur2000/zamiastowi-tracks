import os
import sys
import math
import datetime
import itertools
from datetime import datetime
from datetime import timedelta
from glob import glob
from argparse import ArgumentParser
from pprint import pprint
from collections import *
import xml.etree.ElementTree as ET
from geopy.distance import geodesic
from recordtype import recordtype

fileToFix = 'entire-track-from-mapycz-korekta.gpx'

# read the .gpx file from the dialog here
root = ET.parse(fileToFix).getroot()

configEl = root.findall('./metadata/advance')[0]
advanceTime = int(configEl.get('time'))
advanceElevation = float(configEl.get('elevation'))
date_format_str = '%Y-%m-%dT%H:%M:%SZ'

rTime = ''
rElevation = 0
for idx, el in enumerate(root.findall('./trk/trkseg/trkpt')):
    eleEl = el.find('ele')
    timeEl = el.find('time')
    if idx == 0:
        rTime = timeEl.text
        rElevation = int(eleEl.text)
    else:
        givenTime = datetime.strptime(rTime, date_format_str)
        # Add 15 minutes to datetime object
        newTime = givenTime + timedelta(seconds=advanceTime)
        rTime = newTime.strftime(date_format_str)
        rElevation = rElevation + advanceElevation
    eleEl.text = str(round(rElevation))
    timeEl.text = str(rTime)

# save combined track data into a new file
targetFileName = os.path.join('.', '_tuned_' + fileToFix)
with open(targetFileName, 'wb') as f:
    ET.ElementTree(root).write(f, encoding='utf-8', xml_declaration=True)

print(f'Files combined into >>{targetFileName}<<')
