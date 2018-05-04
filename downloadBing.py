from requests import exceptions
import argparse
import requests
import cv2
import os
import configparser
from os import listdir
from os.path import isfile, join


config = configparser.ConfigParser()
config.sections()
config.read('config.ini')

API_KEY = config['CONFIG']['TOKEN']
MAX_RANGES = 250
GROUP_SIZE = 50

# set the endpoint API URL
URL = "https://api.cognitive.microsoft.com/bing/v7.0/images/search"
EXCEPTIONS = set([IOError, FileNotFoundError,
                  exceptions.RequestException, exceptions.HTTPError,
                  exceptions.ConnectionError, exceptions.Timeout])

# Config
keyword = "mimikyu"
headers = {"Ocp-Apim-Subscription-Key": API_KEY}
params = {"q": keyword, "offset": 0, "count": GROUP_SIZE}

# Start search
print("[INFO] searching images '{}' from Bing API ".format(keyword))
search = requests.get(URL, headers=headers, params=params)
search.raise_for_status()
results = search.json()

numberImages = min(results["totalEstimatedMatches"], MAX_RANGES)
print("[INFO] Had found {} images >> Keyword : '{}'".format(numberImages, keyword))

print("[INFO] Check folder [{}] ...".format(keyword))
directory = os.path.join(os.getcwd(),keyword)
if not os.path.exists(directory):
    print("[INFO] Check folder [{}] there is not exists. ...".format(keyword))
    os.mkdir(directory)
    print("[INFO] Create folder [{}] successful. ...".format(keyword))
# else:
#     onlyfiles = [f for f in listdir(directory) if isfile(join(directory, f))]
#     print(onlyfiles)

count = 0
for offset in range(0, numberImages, GROUP_SIZE):
    print("[INFO] request images no.{}- to no.{}...".format(offset, offset + GROUP_SIZE))
    params["offset"] = offset
    search = requests.get(URL, headers=headers, params=params)
    search.raise_for_status()
    results = search.json()
    test = results["value"]
    listUrls = [img["contentUrl"] for img in results["value"]]
    for url in listUrls:
        print("[INFO] start saving image No. {}...".format(count))
        try:
            print("[INFO] fetching: {}".format(url))
            requestFile = requests.get(url, timeout=30)
            fileName = keyword + '_' + str(count).zfill(6) + url[url.rfind("."):]
            saveDirectory = os.path.join(directory,fileName)
            f = open(saveDirectory, "wb")
            f.write(requestFile.content)
            f.close()
            image = cv2.imread(saveDirectory)

            # if the image is `None` then we could not properly load the
            # image from disk (so it should be ignored)
            if image is None:
                print("[INFO] deleting: {}...".format(fileName))
                os.remove(saveDirectory)
                continue
        except Exception as e:
            print("[ERR] Skipping >> URL {} doesn't load...".format(url))
            print("[ERR] {}... ".format(e))
            continue
        count += 1
