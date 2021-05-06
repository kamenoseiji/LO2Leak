#! /usr/bin/python
import os
UIDfile = open('UIDList')
UIDList = UIDfile.readlines()
UIDfile.close()
fileNum = len(UIDList)
startFile = 0
endFile   = fileNum
for UID in UIDList[startFile:endFile]:
    if UID[0] == '#':   continue
    print UID
    UID = UID.rstrip('\n')
    prefix = UID.replace("/", "_").replace(":","_").replace(" ","")
    if 'spwNames' in locals(): del(spwNames)
    #try:
    if not os.path.isdir('./' + prefix):
        os.system('python ../ScanExporterPlus.py -i BANDPASS -u ' + UID)
    #
    if not os.path.isdir('./' + prefix + '.ms'):
        os.system('asdm2MS ' + prefix)
    #
#
