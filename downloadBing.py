from requests import exceptions
import argparse
import requests
import cv2
import os
import configparser

# ap = argparse.ArgumentParser()
# ap.add_argument("-q", "--query", required=True,
# 	help="search query to search Bing Image API for")
# # ap.add_argument("-k", "--Key", required=True,
# # 	help="txt file to config prgoram API_KEY, MAX_RESULTS, GROUP_SIZE")
# ap.add_argument("-o", "--output", required=True,
# 	help="path to output directory of images")
# args = vars(ap.parse_args())

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
keyword = "BNK48"
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
    os.makedirs(directory)
    print("[INFO] Create folder [{}] successful. ...".format(keyword))

total = 0
for offset in range(0, numberImages, GROUP_SIZE):
    print("[INFO] request images no.{}- to no.{}...".format(offset, offset + GROUP_SIZE))
    params["offset"] = offset
    search = requests.get(URL, headers=headers, params=params)
    search.raise_for_status()
    results = search.json()
    test = results["value"]
    listUrls = [img["contentUrl"] for img in results["value"]]
    for url in listUrls:
        print("[INFO] start saving image No. {}...".format(total))
        try:
            print("[INFO] fetching: {}".format(url))
            requestFile = requests.get(url, timeout=30)
            fileName = keyword + '_' + str(total).zfill(6) + url[url.rfind("."):]
            saveDirectory = os.path.join(directory,fileName)
            f = open(saveDirectory, "wb")
            f.write(requestFile.content)
            f.close()
        except Exception as e:
            print("[ERR] {}... ".format(e))
            continue
        total += 1
