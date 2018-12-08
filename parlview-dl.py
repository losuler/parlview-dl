#!/usr/bin/env python3

import argparse
import random
import cgi
import sys
import xml.etree.ElementTree as etree
from urllib.parse import urlparse, parse_qs
from urllib.request import urlopen, urlretrieve

def argparse_init():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="the URL address of the recording")
    parser.add_argument("format", help="video format to download", default="high", choices=["audio", "low", "med", "high"])
    args = parser.parse_args()
    return args

def extract_id(url):
    parsed = urlparse(url).query
    id = parse_qs(parsed)['videoID'][0]
    return id

def xml_extract(videoId):
    videoXML = "http://parlview.aph.gov.au/player/config5.php?siteID=1&videoID={videoId}&profileIdx=30&ts2=1528111836852".format(videoId=videoId)
    xml = urlopen(videoXML)
    tree = etree.parse(xml)
    root = tree.getroot()
    duration = root.find('playlist/media/info/duration').text
    return duration

def print_formats():
    # TODO: Check are available in the videoXML
    print("Available download qualities:")
    print("audio, low, med, high")
    return

def gen_request():
    random.seed()
    request = random.randrange(2**32)
    return request

def get_filename(downloadURL):
    remoteFile = urlopen(downloadURL)
    resp = remoteFile.info()['Content-Disposition']
    value, params = cgi.parse_header(resp)
    filename = params["filename"]
    return filename

def reporthook(blockNum, blockSize, totalSize):
    readSoFar = blockNum * blockSize
    if totalSize > 0:
        percent = readSoFar * 100 / totalSize
        readSoFarMB = readSoFar / 1000000
        totalSizeMB = totalSize / 1000000
        progress = "\r{:.2f}% {:.2f} MB of {:.2f} MB".format(percent, readSoFarMB, totalSizeMB)
        sys.stderr.write(progress)
        if readSoFar >= totalSize:
            sys.stderr.write("\n")
    else:
        sys.stderr.write("read {}\n".format(readSoFarMB))

def main():
    args = argparse_init()

    videoId = extract_id(args.url)
    duration = xml_extract(videoId)
    request = gen_request()

    format = args.format
    if format == "high":
        format = "h264_2000"
        mux = "1"
    elif format == "med":
        format = "h264_1000"
        mux = "1"
    elif format == "low":
        format = "h264_500"
        mux = "1"
    elif format == "audio":
        format = "mp4_aud"
        mux = "0"

    downloadURL = "http://download.parlview.aph.gov.au/downloads/trim.php?mux={mux}&siteID=1&type={format}&videoID={videoId}&from=0&to={duration}&R={request}&action=directDownload".format(mux=mux, format=format, videoId=videoId, duration=duration, request=request)

    filename = get_filename(downloadURL)
    urlretrieve(downloadURL, filename, reporthook)

main()
