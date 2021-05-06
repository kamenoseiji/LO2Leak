import glob
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
LOG_DIR = './LOGBP/'
NPY_DIR = './NPYBP/'
def SpurFreq( logFileName ):
    logFile = open( logFileName )
    logList = logFile.readlines()
    logFile.close()
    #
    spurSPWList, spurFreqList = [], []
    for logLine in logList:
        logEntry = logLine.split()
        if logEntry[0] == 'SPW':
            spurSPWList  = spurSPWList  + [int(logEntry[1])]
            spurFreqList = spurFreqList + [float(logEntry[8])]
        #
    #
    return spurSPWList, spurFreqList
#
def GetAntList(prefix):
    AntNPYList = glob.glob(NPY_DIR + prefix + '*.Ant.npy')
    if len(AntNPYList) == 0: return np.array([])
    antList = np.load(AntNPYList[0])
    return antList
#
def SpecSPW(prefix, spw):
    BPNPYList = glob.glob(NPY_DIR + prefix + '*-SPW' + `spw` + '-BPant.npy')
    if len(BPNPYList) == 0: return np.array([]), np.array([])
    FreqFile = NPY_DIR + prefix + '-SPW' + `spw` + '-Freq.npy'
    if not os.path.isfile(FreqFile): return np.array([]), np.array([])
    freq  = np.load(FreqFile)
    BPant = np.load(BPNPYList[0])
    return freq, BPant
#
def detectSpur(spurFreq, spwFreq, spwBP):
    spurSNR = 0.0
    chNum, BW, chWid = len(spwFreq), max(spwFreq) - min(spwFreq), abs(np.median(np.diff(spwFreq)))
    chRange = range(chNum)
    if BW > 1.875: chRange = range(int(0.05*chNum), int(0.95*chNum))
    spurCH = np.where( abs(spwFreq - spurFreq) < chWid)[0].tolist()
    if (spurCH[0]-1 in chRange) and (spurCH[-1]+1 in chRange) :
        spurProCH = [spurCH[0] -1] + spurCH + [spurCH[-1] +1]   # Spur Line Profile channels
        spurBLCH  = range(max(spurCH + [17]) - 17, max(spurCH + [3]) - 3) + range(min(spurCH + [chNum-3]) + 3, min(spurCH + [chNum-16]) + 16)
        spurProf, resid = quadraFit( spwFreq[spurProCH], abs(spwBP[spurProCH]), spurFreq)
        baseProf, resid = quadraFit( spwFreq[spurBLCH],  abs(spwBP[spurBLCH]),  spurFreq)
        spurSNR = abs(spurProf[0] - baseProf[0])/resid
    #
    return spurSNR
#
def quadraFit( freq, amp, refFreq ):
    relFreq = freq - refFreq
    P = np.array([np.ones(len(relFreq)), relFreq, relFreq**2] )
    Pinv = np.linalg.inv(P.dot(P.T))
    solution = Pinv.dot( P.dot(amp).T )
    resid    = amp - (solution[0] + solution[1]*relFreq + solution[2]*relFreq**2)
    return solution, np.std(resid)
#

UIDfile = open('UIDList')
UIDList = UIDfile.readlines()
UIDfile.close()
fileNum = len(UIDList)
startFile = 0
endFile   = fileNum
polName = ['X', 'Y']
snrThresh = 5.0
spurLog = open('LO2Spur.log', 'w')
text_sd = 'Ant SPW POL Freq  SNR  UID'
spurLog.write(text_sd + '\n'); print text_sd
for UID in UIDList[startFile:endFile]:
    if UID[0] == '#':   continue
    UID = UID.rstrip('\n')
    prefix = UID.replace("/", "_").replace(":","_").replace(" ","")
    antList = GetAntList(prefix)
    if len(antList) == 0: continue
    logFileName = LOG_DIR + prefix + '-LO2Spur.log'
    if not os.path.isfile(logFileName): continue
    #print logFileName
    spurSPWList, spurFreqList = SpurFreq(logFileName)
    for spurIndex in range(len(spurFreqList)):
        spwFreq, spwBP = SpecSPW(prefix, spurSPWList[spurIndex])
        if len(spwFreq) == 0: continue
        spwFreq = 1.0e-9* spwFreq
        antNum, polNum, chNum = spwBP.shape[0], spwBP.shape[1], spwBP.shape[2]
        #if chNum < 64: continue
        if chNum < 256: continue
        for ant_index in range(antNum):
            for pol_index in range(polNum):
                spurSNR = detectSpur(spurFreqList[spurIndex], spwFreq, spwBP[ant_index, pol_index])
                if spurSNR > snrThresh:
                    text_sd = '%s %d %s %.3f %4.1f %s' % (antList[ant_index], spurSPWList[spurIndex], polName[pol_index], spurFreqList[spurIndex], spurSNR, prefix)
                    spurLog.write(text_sd + '\n'); print text_sd
                    pp = PdfPages('SP_' + prefix + '_' + antList[ant_index]+ '_SPW' + `spurSPWList[spurIndex]` + '_POL-' + polName[pol_index] + '.pdf')
                    figSP = plt.figure(figsize = (11, 8))
                    figSP.suptitle(prefix + ' ' + antList[ant_index] + ' SPW' + `spurSPWList[spurIndex]` + ' POL-' + polName[pol_index])
                    figSP.text(0.45, 0.05, 'Frequency [GHz]')
                    figSP.text(0.03, 0.5, 'Bandpass Amplitude', rotation=90)
                    BPPL = figSP.add_subplot(1, 2, 1)
                    SPPL = figSP.add_subplot(1, 2, 2)
                    spurCH = np.argmin(abs(spwFreq - spurFreqList[spurIndex]))
                    plotSpurCH = range(max([16, spurCH])-16, min([chNum-16,spurCH])+16)
                    BPPL.axvspan(xmin=spwFreq[plotSpurCH[0]], xmax=spwFreq[plotSpurCH[-1]], color='gray', alpha=0.5)
                    BPPL.plot(spwFreq, abs(spwBP[ant_index, pol_index]), ls='steps-mid')
                    SPPL.vlines(x=spurFreqList[spurIndex], ymin=min(abs(spwBP[ant_index, pol_index])[plotSpurCH]), ymax=max(abs(spwBP[ant_index, pol_index])[plotSpurCH]), color='gray')
                    SPPL.plot(spwFreq[plotSpurCH], abs(spwBP[ant_index, pol_index])[plotSpurCH], ls='steps-mid')
                    SPPL.text(spurFreqList[spurIndex], max(abs(spwBP[ant_index, pol_index])[plotSpurCH]), 'SNR=%.1f at %.3f GHz' % (spurSNR, spurFreqList[spurIndex]))
                    plt.show()
                    figSP.savefig(pp, format='pdf')
                    plt.close('all')
                    pp.close()
                #
            #
        #
    #
#
spurLog.close()
