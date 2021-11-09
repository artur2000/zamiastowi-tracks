import os
import sys
import pprint
from xml.etree import ElementTree as ET
from timecode import Timecode
from edl import Parser
from recordtype import recordtype

pp = pprint.PrettyPrinter(indent=4)
namespace = 'http://www.topografix.com/GPX/1/1'
# frame rate one of ['60', '59.94', '50', '30', '29.97', '25', '24', '23.98']
projectFrameRate = '29.97'
srcTcOffsetReference = '10:50:35:26'

TimelineEvent = recordtype('TimelineEvent', [('event_no', 0), ('clip_name', 0), ('rec_start_tc', 0), ('rec_end_tc', 0),
                                             ('src_start_tc', 0), ('src_end_tc', 0)])

class XMLCombiner(object):
    def __init__(self, filenames):
        assert len(filenames) > 0, 'No filenames!'
        self.filenames = []
        # save all the roots, in order, to be processed later
        self.roots = []
        for f in filenames:
            filePath = f"./telemetry/{f}"
            if (os.path.exists(filePath)):
                self.filenames.append(os.path.basename(f).split('.')[0])
                self.roots.append(ET.parse(filePath).getroot())

    def combine(self):
        firstName = self.roots[0].findall(".//{"+ namespace + "}name")[0]
        firstName.text = ' + ' . join(self.filenames)
        xpathSearchString = ".//{"+ namespace + "}trkseg"
        firstElement = self.roots[0].findall(xpathSearchString)
        for r in self.roots[1:]:
            otherElement = r.findall(xpathSearchString)
            # combine each element with the first one, and update that
            self.combine_element(firstElement[0], otherElement[0])
        # return the string representation
        return self.roots[0]

    def combine_element(self, one, other):
        """
        This function recursively updates either the text or the children
        of an element if another element is found in `one`, or adds it
        from `other` if not found.
        """
        # Create a mapping from tag name to element, as that's what we are fltering with
        mapping = {el.tag: el for el in one}
        for el in other:
            # Add it
            one.append(el)


def get_track_files_to_combine_txt(filePath):
    with open(filePath) as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]
    return lines

def get_track_files_to_combine_fcpxml(filePath):
    root = ET.parse(filePath).getroot()
    clips = []
    for type_tag in root.findall('./library/event/project/sequence/spine/asset-clip'):
        clips.append(type_tag.get('name') + '.gpx')
    return clips

"""
@see https://github.com/simonh10/python-edl
required:
> pip install timecode
> pip install edl
"""
def get_track_files_to_combine_edl(filePath, frameRate):
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
    if (os.path.exists('./combine-clip-tracks.edl')):
        clips, timelineEvents = get_track_files_to_combine_edl('./combine-clip-tracks.edl', projectFrameRate)
    elif (os.path.exists('./combine-clip-tracks.fcpxml')):
        clips = get_track_files_to_combine_fcpxml('./combine-clip-tracks.fcpxml')
    elif (os.path.exists('./combine-clip-tracks.txt')):
        clips = get_track_files_to_combine_txt('./combine-clip-tracks.txt')

    # combine the track files
    ET.register_namespace('', "http://www.topografix.com/GPX/1/1")
    et = XMLCombiner(clips).combine()

    # save combined track data into a new file
    targetFileName = os.path.join('.', 'telemetry', '_combined-track.gpx')
    with open(targetFileName, 'wb') as f:
        ET.ElementTree(et).write(f, encoding='utf-8', xml_declaration=True)

    print(f'Files combined into >>{targetFileName}<<')
