# Image grabber - gets the URL of a page and extracts the image URLS...
import random

import requests;
from bs4 import BeautifulSoup;
import time;
import os;
import argparse;

parser = argparse.ArgumentParser("main.py")
parser.add_argument("URL", help="A URL to get the images from.", type=str)
parser.add_argument("mode", help="Mode. 1 = IMG SRC, 2 = Links HREF", type=int)

args = parser.parse_args()
URL = args.URL
#Sanitise URL
if (len(URL) < 4):
    print("URl too short!")
    exit(1)
else:
    if (URL[:4] != "http"):
        print("Warning - missing http in address. Adding this time...")
        URL = "http://" + URL
print(f"URL is {URL}")
mode = args.mode
tag_to_find = ""
element_to_find = ""
if (mode == 2):
    tag_to_find = "a"
    element_to_find = "href"
if (mode == 1):
    tag_to_find = "img"
    element_to_find = "src"


page = requests.get(URL);
#print(page.content)

soup = BeautifulSoup(page.content,"html.parser")
image_tags = soup.findAll(tag_to_find)
a = 0;
print(f"Found {len(image_tags)} matching elements...")
found_list = []
for tag in image_tags:
    a = a + 1

    pause = random.randrange(4, 12)


    fileType = tag[element_to_find][-3:]
    if (fileType == 'jpg'):
        if (not tag[element_to_find] in found_list):

            if (tag[element_to_find][-5:] != 's.jpg'):
                print("")
                print(f"We are on {a} of {len(image_tags)}")
                print(f"Pausing for {pause} seconds to avoid freaking out the server...")
                time.sleep(pause)
                print(f"Getting:{tag[element_to_find]}...")
                req_url = tag[element_to_find]
                if (req_url[:4] != "http"):
                    #print(f"No HTTP element found. {req_url[:4]} found instead.")
                    r = requests.get("https:" + tag[element_to_find])
                else:
                    r = requests.get(tag[element_to_find])
                f = tag[element_to_find]
                split_fName = f.split("/")
                fName = split_fName[-1]
                b = 0;
                while (os.path.isfile(fName)):
                    print("File exists. Renaming to avoid overwrite...")
                    first = fName.split(".")[0];
                    first = first + "_" + str(b) + "."
                    fName = first + fileType
                    b = b + 1
                file = open(fName, "wb")
                print(f"Writing {fName}...")
                file.write(r.content);
                file.close();
                print("File written.")
                found_list.append(tag[element_to_find])

            else:
                print("Skipping thumbnail.")
        else:
            print("Skipping duplicate.")



print("Done!")
