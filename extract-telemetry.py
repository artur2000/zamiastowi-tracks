# This script extracts GoPro telemetry data from all files inside the same directory
# 1) ffmpeg must be installed first
# 2) https://github.com/JuanIrache/gopro-utils must be installed first
# PLace the script into a directory with GoPro footage and run it
# For each file filename.MP4 a bin file filename.MP4.bin will be created

import os
import sys
from os import listdir
from os.path import isfile, join
import pathlib

pathlib.Path("./telemetry").mkdir(parents=True, exist_ok=True)

mypath = pathlib.Path(__file__).parent.resolve()

onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

for filename in onlyfiles:
	if filename.endswith('.MP4') or filename.endswith('.mp4'):	
		cmd = 'ffmpeg -y -i ' + filename + ' -codec copy -map 0:3 -f rawvideo ./telemetry/' + filename + '.bin'
		print(cmd)
		os.system(cmd)
		cmd = 'gpmd2csv -i ./telemetry/' + filename + '.bin -o ./telemetry/' + filename + '.csv'
		print(cmd)
		os.system(cmd)
		cmd = 'gopro2gpx -i ./telemetry/' + filename + '.bin -o ./telemetry/' + filename + '.gpx'
		print(cmd)
		os.system(cmd)

