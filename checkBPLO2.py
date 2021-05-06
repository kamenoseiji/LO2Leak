SCR_DIR = '/users/skameno/ALMA_SV/'
R_DIR = '/usr/bin/'
TBL_DIR = 'http://www.alma.cl/~skameno/AMAPOLA/Table/'
execfile(SCR_DIR + 'interferometry.py')
execfile(SCR_DIR + 'ASDM_XML.py')
wd = './'
QUMODEL = True
COMPDB = False
PLOTTAU = True
PLOTTSYS = True
BPPLOT   = True
TSYSCAL = True
UIDfile = open('UIDList')
UIDList = UIDfile.readlines()
UIDfile.close()
fileNum = len(UIDList)
startFile = 0
endFile   = fileNum
#bunchNum = 2
for UID in UIDList[startFile:endFile]:
    if UID[0] == '#':   continue
    UID = UID.rstrip('\n')
    prefix = UID.replace("/", "_").replace(":","_").replace(" ","")
    print prefix
    if 'spwNames' in locals(): del(spwNames)
    #try:
    if not os.path.isdir('./' + prefix):
        os.system('asdmExport ' + UID)
    #
    if CheckCorr(prefix) == 'ALMA_ACA': continue
    if not os.path.isdir('./' + prefix + '.ms'):
        importasdm(prefix)
    #
    #msfile = prefix + '.ms'
    #atmSPWs = GetAtmSPWs(msfile)
    #antFlag = []
    execfile(SCR_DIR + 'checkLO2.py')
    spwListS = GetBPcalSPWs(msfile)
    BPscan = GetBPcalScans(msfile)[0]
    for spw in spwListS:
        antFlag = []
        spwList = [spw]
        execfile(SCR_DIR + 'checkBP.py')
        os.system('mv BP_' + prefix + '_REF' + antList[UseAnt[refantID]] + '_Scan' + `BPscan` + '.pdf BP_' + prefix + '_REF' + antList[UseAnt[refantID]] + '_Scan' + `BPscan` + '_SPW' + `spw` + '.pdf')
    #
    os.system('mv *.npy NPY/')
    os.system('mv *.pdf PDF/')
    os.system('mv *.log LOG/')
    del spwListS, atmSPWs, BPscan, atmspwLists, atmscanLists, bandAtmSPWs, atmBandNames
    #os.system('rm -rf *.cl')
    #os.system('rm -rf ' + prefix)
    #os.system('rm -rf ' + prefix + '.ms')
#
