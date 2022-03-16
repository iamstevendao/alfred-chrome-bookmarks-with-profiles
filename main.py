#!/usr/bin/env python

import os
import json

def get_bookmarks(browser, path):
  bookmarks = []
  if os.path.isdir(path) == False:
    return bookmarks
  folders = [ name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name)) ]
  for folder in folders:
    profileFile = "{}/{}/Preferences".format(path, folder)
    if folder != 'System Profile' and os.path.isfile(profileFile):
      with open(profileFile) as pf:
        data = json.load(pf)
        profileName = data['profile']['name']
        bookmarkFile = "{}/{}/Bookmarks".format(path, folder)
        if folder != 'System Profile' and os.path.isfile(bookmarkFile):
          with open(bookmarkFile) as bf:
            data = json.load(bf)
            for child in data['roots']['bookmark_bar']['children']:
              bookmarks.append({
                "icon": {
                  "path": "{}/{}/Google Profile Picture.png".format(path, folder)
                },
                "arg": child['url'],
                "variables": {
                  "browser": browser['name'],
                  "profile": folder,
                },
                "subtitle": "{} - Bookmarks Bar: {}".format(profileName, child['url']),
                "title": "{}".format(child['name']),
                "match": "{} {} Bookmarks Bar {}".format(child['name'], profileName, child['url']),
              })

            for topChild in data['roots']['other']['children']:
              for child in topChild['children']:
                bookmarks.append({
                  "icon": {
                    "path": "{}/{}/Google Profile Picture.png".format(path, folder)
                  },
                  "arg": child['url'],
                  "variables": {
                    "browser": browser['name'],
                    "profile": folder,
                  },
                  "subtitle": "{} - {}: {}".format(profileName, topChild['name'], child['url']),
                  "title": "{}".format(child['name']),
                  "match": "{} {} {} {}".format(child['name'], profileName, topChild['name'], child['url']),
                })
  return bookmarks


home = os.path.expanduser("~")

browsers = [
  { 'name': 'CHROME', 'path': '/Library/Application Support/Google/Chrome', 'icon': 'chrome.icns' },
]

bookmarks = []

for browser in browsers:
  path = "{}/{}".format(home, browser['path'])
  prof = get_bookmarks(browser, path)
  bookmarks += prof

print(json.dumps({"items": bookmarks}, indent=2))
