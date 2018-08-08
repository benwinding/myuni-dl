#!/usr/bin/python

# Log into course course page at myuni.adelaide.edu
# Save all the files from the modules page

# usage:
#   python scrap-lectures.py --course 11111 --username a1111111 --password aaaaaaaaaaa 
# 
# NOTE: passwords must be wrapped in quotes '*98234^%$65%$#$##'
# 
# optional:
#   --type pdf
#   --type zip

import argparse
# Get command line arguments
parser = argparse.ArgumentParser()
optional = parser._action_groups.pop()
required = parser.add_argument_group('required arguments')
required.add_argument('--course', help='input course page file, eg urls.txt', required=True)
required.add_argument('--username', help='uni id, eg: a11111111', required=True)
required.add_argument('--password', help="uni password, eg: 'pa$$word'", required=True)
optional.add_argument('--downloadOnly', help='specific file type to be downloaded eg: zip, pdf, doc', default='all', type=str)
parser._action_groups.append(optional)
args = parser.parse_args()

# Helper functions
import shutil, os, errno
def make_path(path):
    try:
        print("Making Folder: " + path)
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text 

# Start scraping
from robobrowser import RoboBrowser
import re
import urlparse

courseModulesUrl = 'https://myuni.adelaide.edu.au/courses/' + args.course + '/modules'
browser = RoboBrowser(history=True, parser='html.parser')
browser.open(courseModulesUrl)
# Handle login page
form = browser.get_form(id='fm1')
form["username"] = args.username
form["password"] = args.password
browser.session.headers['Referer'] = args.course
browser.submit_form(form)
# Get course name (no special characters)
courseTitle = browser.find("title").text
courseTitle = remove_prefix(courseTitle, 'Course Modules: ')
courseTitle = "".join([x if x.isalnum() else "_" for x in courseTitle])
print('Course Url: ' + courseModulesUrl)
print('Course Title: ' + courseTitle)
print('Finding file links of type: ' + args.downloadOnly)
# Make output dir
outputDir = os.path.join('output/', courseTitle)
make_path(outputDir)
# Get modules links with lecture in title
moduleLinks = browser.find_all("a", { "class" : "for-nvda" })

print('Found ' + str(len(moduleLinks)) + ' links, (not all will be valid)')

# Process each lecture link
for moduleLink in moduleLinks:
    print('Opening: ' + moduleLink['aria-label'])
    browser.follow_link(moduleLink)
    try:
        # Find link - containing words "download"
        downloadLinkRel = browser.find('a', href = re.compile(r'.*download*'))
        # If failed, find link - containing reference to file "****.XXX"
        if downloadLinkRel is None: 
            downloadLinkRel = browser.find('a', href = re.compile(r'.*\.[a-z]{3,4}$'))
        fileNameWithExtension = downloadLinkRel.text.strip()
        # Check the link is the right filetype
        if args.downloadOnly != 'all' and not fileNameWithExtension.endswith(args.downloadOnly):
            print('   not processing (wrong extension): ' + fileNameWithExtension)
            continue
        downloadLinkAbsolute = urlparse.urljoin(courseModulesUrl, downloadLinkRel['href'])
        pdfOutputPath = os.path.join(outputDir, fileNameWithExtension)
        # Check if file already download (incase the tool was interrupted)
        if os.path.isfile(pdfOutputPath):
            print('   file already downloaded')
            continue
        # Download file from link to local
        print('   downloading: ' + downloadLinkAbsolute)
        request = browser.session.get(downloadLinkAbsolute, stream=True)
        with open(pdfOutputPath, "wb") as pdfFile:
            pdfFile.write(request.content)
        print('   saved at: ' + pdfOutputPath)
    except AttributeError as exception:
        print("   couldn't find a download link here ...")
        continue
