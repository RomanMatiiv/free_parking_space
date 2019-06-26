import os
from os import walk
import xml.etree.ElementTree as ET
from tqdm import tqdm
from argparse import ArgumentParser
import logging

logging.basicConfig(level=logging.INFO)

logging.info("start read params from console")
parser = ArgumentParser()
parser.add_argument("-d", "--data", dest="path_to_data", default="")
parser.add_argument("-o", "--out", dest="path_to_output", default="")
args = parser.parse_args()

PATH_TO_FOLDER = args.path_to_data
PATH_TO_OUTPUT = args.path_to_output

if not os.path.isdir(PATH_TO_FOLDER):
    raise IOError("Folder with data dosn't exist")

logging.info("start search all xml files")
files = []
for (dirpath, dirnames, filenames) in walk(PATH_TO_FOLDER):
    for cur_filename in filenames:
        if cur_filename.endswith('.xml'):
            files.append(os.path.join(dirpath, cur_filename))

unlabled = 0

logging.info("start writing info to output file")
with open(PATH_TO_OUTPUT, "w") as f:
    for file in tqdm(files):

        tree = ET.parse(file)
        root = tree.getroot()

        for elem in root:

            try:
                elem.attrib["occupied"]
            except KeyError:
                unlabled += 1
                continue

            if elem.attrib["occupied"] == "1":
                rotatedRect, contour = elem.getchildren()
                all_x = []
                all_y = []

                for point in contour.getchildren():
                    all_x.append(int(point.attrib["x"]))
                    all_y.append(int(point.attrib["y"]))

                x1 = min(all_x)
                y1 = min(all_y)

                x2 = max(all_x)
                y2 = max(all_y)

                file = file.replace(".xml", ".jpg")

                row_elements = [file, str(x1), str(y1), str(x2), str(y2), "car"]
                row = ",".join(row_elements)

                f.write(row)
                f.write("\n")


print("Parking space unlabling: ", unlabled)
logging.info("finished")
