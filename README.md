# Introduction 
This repo contains scripts to modify/convert exported files from Subsurface Divelogs software.

# Divesites_sorter.py: 
- Written in Python 3.12.1 advised is to use Python 3.8 or higher.
- Modules sys,os,xml,csv are all standard installed.
- On simple double click it expects an input file named Divesites.xml in the same directory.
- input path and mode can be changed via command line
- output path is the same as input path but with "_sorted" in the name
- commandline help: "Divesites_sorter.py -h"
- default mode is set in the "__main__" at "mode = 'csv'"
- "mode = 'xml_extend'" creates an import compatible xml but with extra divesite properties.
- xml_extend is useful as a sorted backup of all your sites.
- The top level function after "main" logic is "convert_divesites"
- sorting/addition is done by "sort_divesites" and optionally "divesites2csv" is called.

# Useful:

## Anonymous divesite uuid: (Notepad++)
Replace action with Regular expression:
uuid='\s*\w*'
with:
uuid=''
Test: uuid=' 67a9af6'

## Truncate (google) gps to 6 decimals: (Notepad++)
\d{1,2}\.\d{6}\K\d+
Replace with nothing and replace all.
Test: 26.640739144242012, 34.061670247436794

## coordinates system converter
https://coordinates-converter.com/en/decimal/26.640739,34.061670?karte=OpenStreetMap&zoom=13

## Dutch Divesites info
https://people.zeelandnet.nl/delta48/hi/dutch/coordinaten.htm
https://www.anemoon.org/DesktopModules/Bring2mind/DMX/API/Entries/Download?command=core_download&entryid=1120&language=nl-NL&PortalId=0&TabId=165
