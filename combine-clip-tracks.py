import os
import sys
import pprint
from xml.etree import ElementTree as ET

pp = pprint.PrettyPrinter(indent=4)
namespace = 'http://www.topografix.com/GPX/1/1'

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
        author = self.roots[0].findall(".//{"+ namespace + "}author")[0]
        author.text = os.path.basename(__file__)
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
    # read the .gpx file from the dialog here
    root = ET.parse(filePath).getroot()

    clips = []
    for type_tag in root.findall('./library/event/project/sequence/spine/asset-clip'):
        clips.append(type_tag.get('name') + '.gpx')
    return clips    

if __name__ == '__main__':

    # read which track files to combine
    if (os.path.exists('./combine-clip-tracks.fcpxml')):
        lines = get_track_files_to_combine_fcpxml('./combine-clip-tracks.fcpxml')  
    elif (os.path.exists('./combine-clip-tracks.txt')):
        lines = get_track_files_to_combine_csv('./combine-clip-tracks.txt')  

    # combine the track files
    ET.register_namespace('', "http://www.topografix.com/GPX/1/1")
    et = XMLCombiner(lines).combine()

    # save combined track data into a new file
    targetFileName = os.path.join('.', 'telemetry', '_combined-track.gpx')
    with open(targetFileName, 'wb') as f:
        ET.ElementTree(et).write(f, encoding='utf-8', xml_declaration=True)

    print(f'Files combined into >>{targetFileName}<<')
