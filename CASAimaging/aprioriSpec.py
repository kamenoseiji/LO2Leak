SCR_DIR = '/home/skameno/ALMA_SV/'
wd = './'
DELAYCAL = False
BPPLOT   = True
antFlag = []
PLOTFMT  = 'pdf'
polName = ['XX', 'YY']
spwList  = [25, 27, 29, 31]
#BPscan = 3
prefix = 'uid___A002_Xd3e89f_X83c3'
msfile = prefix + '.ms'
antNum = 45
execfile(SCR_DIR + 'aprioriSpec.py')
