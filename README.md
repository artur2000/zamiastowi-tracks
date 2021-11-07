Extract telemetry data from gopro footage
=========================================

script: extract-telemetry.py

For this script to be usefull we need a 3rd party software first

1) Compile and install a go lang script from here: https://github.com/JuanIrache/gopro-utils
2) I downloaded the tools here: F:\audio-video-production\tools\gopro-utils
3) I compiled two of the tools and added those paths into Path environment variable
F:\audio-video-production\tools\gopro-utils\bin\gopro2gpx
F:\audio-video-production\tools\gopro-utils\bin\gpmd2csv

Now the workflow how to use this script:

1) Put all gopro footage for one zamiastowi track project (one journey for one video) into one directory
2) Put this script into that directory
3) Run this script from within this directory
4) the script should use the compiled gps tools to create a subdirectory "telemetry" and export the telemetry data for each video file found in the current footage directory
5) We are interested in the .gpx files with the GPS data from the gopro footage

Merge all telemtry data from all clips into one track .gpx file
===============================================================

script: combine-clip-tracks.py

1) Put this script into the directory holding the journey gopro footage along with extracted GPS telemetry data
2) Now we need to tell this script which .gpx files should be merged. 
2.1) We can do it manually by providing a file called combine-clip-tracks.txt in the same directory, putting each .gpx file name in a new line. The merge script will merge those files in the given order
2.2) Better option: we can extract the clip names from our rough cut timeline in resolve. To use this we must first create a rough cut in the cut page of resolve. Then we export the timeline into the format "FCPXML 1.9". file -> Export -> Timeline... -> as "FCPXML 1.9 file (*.fcpxml)". We save this file with the name combine-clip-tracks.fcpxml in the same directoru as the script.
3) We run the script
4) The merged file will be written into "telemetry/_combined-track.gpx"
