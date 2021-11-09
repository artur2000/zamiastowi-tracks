"""

"""
import os
import argparse
import sys
import pprint
from xml.etree import ElementTree as ET
from timecode import Timecode
from edl import Parser
from recordtype import recordtype

# Construct the argument parser
ap = argparse.ArgumentParser()

# Add the arguments to the parser
ap.add_argument("-f", "--file", required=True,
                help="EDL file")
args = vars(ap.parse_args())

pp = pprint.PrettyPrinter(indent=4)
namespace = 'http://www.topografix.com/GPX/1/1'
# frame rate one of ['60', '59.94', '50', '30', '29.97', '25', '24', '23.98']
projectFrameRate = '29.97'
srcTcOffsetReference = '10:50:35:26'

TimelineEvent = recordtype('TimelineEvent', [('event_no', 0), ('clip_name', 0), ('rec_start_tc', 0), ('rec_end_tc', 0),
                                             ('src_start_tc', 0), ('src_end_tc', 0)])

"""
@see https://github.com/simonh10/python-edl
required:
> pip install timecode
> pip install edl
"""
def get_track_files_edl(filePath, frameRate):
    parser = Parser(frameRate)
    events = []
    clips = []

    with open(filePath) as f:
        edl = parser.parse(f)
        for event in edl.events:
            tEvent = TimelineEvent()
            tEvent.event_no = str(event.num)
            tEvent.clip_name = str(event.clip_name)
            tEvent.rec_start_tc = str(event.rec_start_tc).replace(';', ':')
            tEvent.rec_end_tc = str(event.rec_end_tc).replace(';', ':')
            tEvent.src_start_tc = str(event.src_start_tc).replace(';', ':')
            tEvent.src_end_tc = str(event.src_end_tc).replace(';', ':')
            pp.pprint(tEvent)
            events.append(tEvent)
            clips.append(str(event.clip_name) + '.gpx')
    # write the
    return clips, events

if __name__ == '__main__':

    clips = []
    timelineEvents = []

    # read which track files to combine
    edlFile = os.path.exists(args['file'])
    if (edlFile):
        clips, timelineEvents = get_track_files_edl('./combine-clip-tracks.edl', projectFrameRate)

    # save the list of clip files used in the timeline into a text file
    if (len(timelineEvents) > 0):
        targetFileName = os.path.join('.', '_timeline-clips-list.csv')
        with open(targetFileName, 'w') as f:
            f.write("num;clip_name;src_start_tc;src_end_tc;rec_start_tc;rec_end_tc;rec_start_tc_offset\n")
            for timelineEvent in timelineEvents:
                tc1 = Timecode(projectFrameRate, srcTcOffsetReference)
                tc2 = Timecode(projectFrameRate, timelineEvent.src_start_tc)
                if (tc2 > tc1):
                    print(str(timelineEvent.rec_start_tc), ' - ', str(srcTcOffsetReference))
                    recTcOffset = tc2 - tc1
                else:
                    recTcOffset = 0
                f.write(';'.join([timelineEvent.event_no, timelineEvent.clip_name, timelineEvent.src_start_tc,
                                  timelineEvent.src_end_tc, timelineEvent.rec_start_tc,
                                  timelineEvent.rec_end_tc, str(recTcOffset).replace(';', ':')]) + "\n")
            f.close()
    else:
        targetFileName = os.path.join('.', '_timeline-clips-list.txt')
        with open(targetFileName, 'w') as f:
            for clip in clips:
                f.write(clip + "\n")
            f.close()

    print(f'Result written into >>{targetFileName}<<')
