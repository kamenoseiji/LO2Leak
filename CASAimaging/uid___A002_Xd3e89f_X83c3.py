prefix = 'uid___A002_Xd3e89f_X83c3'
REFANT = 'DV08'
BPCAL = 'J1427-4206'
PHCAL = 'J1246-2547'
CHECK = 'J1305-2850'
TARGET = 'R_Hya'
'''
os.system('rm -rf ' + prefix + '_flagonline.txt')    
importasdm(prefix)
plotants( vis=prefix + '.ms', figfile=prefix + '_plotants.png')
#
#
flagdata(vis=prefix + '.ms', mode='manual', spw='0~32', autocorr=True, flagbackup = False)
flagdata(vis=prefix + '.ms', mode='manual', intent = '*POINTING*,*ATMOSPHERE*', flagbackup = False)
flagmanager(vis=prefix+'.ms', mode='save', versionname='Apriori')
#
#-------- Tsys 
from recipes.almahelpers import tsysspwmap
os.system('rm -rf cal.' + prefix + '.tsys')
gencal(vis=prefix+'.ms', caltype='tsys', caltable='cal.'+prefix+'.tsys')
plotcal(caltable='cal.'+prefix+'.tsys', xaxis='freq', yaxis='tsys', spw='17:3~124,19:3~124,21:3~124,23:3~124', iteration='antenna', subplot=221)
#-------- WVR 
os.system('rm -rf cal.' + prefix + '.WVR')
wvrgcal(segsource=True, caltable='cal.'+prefix+'.WVR', vis=prefix+'.ms', wvrspw=[4], tie=[BPCAL + ',' + PHCAL+ ',' + CHECK + ',' + TARGET], toffset=0, wvrflag=[], statsource=TARGET)
plotcal('cal.'+prefix+'.WVR', xaxis='time',yaxis='phase',iteration='antenna', subplot=221)
#
tsysmap = tsysspwmap(vis=prefix+'.ms', tsystable='cal.'+prefix+'.tsys', tsysChanTol=1)
for fields in [BPCAL, PHCAL, TARGET]:
    applycal(vis=prefix+'.ms', field=fields, flagbackup=False, spw='25,27,29,31', interp=['linear', 'nearest'], gaintable=['cal.'+prefix+'.tsys', 'cal.'+prefix+'.WVR'], gainfield=fields, spwmap=[tsysmap, []], calwt=True)
applycal(vis=prefix+'.ms', field=CHECK, flagbackup=False, spw='25,27,29,31', interp=['linear', 'nearest'], gaintable=['cal.'+prefix+'.tsys', 'cal.'+prefix+'.WVR'], gainfield=[TARGET, CHECK], spwmap=[tsysmap, []], calwt=True)
#-------- Split
os.system('rm -rf '+prefix+'_line.ms*'); split(vis=prefix+'.ms', outputvis=prefix+'_line.ms', datacolumn='corrected', spw='25,27,29,31')
#-------- Phase Cal for bandpass
os.system('rm -rf P0*')
gaincal(vis=prefix+'_line.ms', caltable='P0', spw='*', field= BPCAL, scan='', selectdata=True, solint='int', refant=REFANT, calmode='p')
plotcal(caltable = 'P0', xaxis = 'time', yaxis = 'phase', plotsymbol='.', plotrange = [0,0,-180,180], iteration = 'antenna', figfile='P0.phase.png', subplot = 221)
os.system('rm -rf B0*')
bandpass(vis = prefix + '_line.ms', caltable = 'B0', gaintable='P0', spw='*', field= BPCAL, scan='', minblperant=5, minsnr=5, solint='inf', bandtype='B', fillgaps=1, refant = REFANT, solnorm = True, spwmap=[0,1,2,3])
plotbandpass(caltable = 'B0', xaxis='freq', yaxis='amp', plotrange = [0,0,0,1.2], figfile='B0.png')
plotbandpass(caltable = 'B0', xaxis='freq', yaxis='phase',plotrange = [0,0,-180.0,180.0], figfile='B0.png')
#-------- Phase Cal for all
os.system('rm -rf P1*')
gaincal(vis=prefix+'_line.ms', caltable='P1', spw='*', gaintable = ['B0','P0'], field=BPCAL + ', ' +  PHCAL + ',' + CHECK, selectdata=True, solint='int', refant=REFANT, gaintype='T', combine='spw', calmode='p', minsnr=3)
plotcal(caltable = 'P1', xaxis = 'time', yaxis = 'phase', plotsymbol='.', plotrange = [0,0,-180,180], iteration = 'antenna', figfile='cal_phase.png', subplot = 221)
#-------- Flux cal
au.getALMAFlux(BPCAL, 230.07939217, date='2018-10-25', showplot=True)
os.system('rm -rf G0*')
setjy(vis = prefix + '_line.ms', field=BPCAL, spw='0,1,2,3', standard='manual', fluxdensity=[2.06031577678287,0,0,0], spix = [-0.583939, 0], usescratch=False)
gaincal(vis = prefix + '_line.ms', caltable = 'G0', spw ='*', field = BPCAL + ',' + PHCAL + ',' + CHECK, minsnr=5.0, solint='inf', selectdata=True, solnorm=False, refant = REFANT, gaintable = ['B0','P0','P1'], spwmap=[[0,1,2,3],[0,1,2,3],[0,0,0,0]], calmode = 'a')
plotcal(caltable = 'G0', xaxis = 'time', yaxis = 'amp', plotsymbol='o', plotrange = [], iteration = 'antenna', figfile='G0.png', subplot = 221)
fluxscale(vis= prefix + '_line.ms', caltable='G0', fluxtable='G0.flux', reference=BPCAL, transfer=CHECK + ', ' +  PHCAL, refspwmap=[0,1,2,3])
#2021-03-20 02:35:40 INFO fluxscale	Beginning fluxscale--(MSSelection version)-------
#2021-03-20 02:35:40 INFO fluxscale	 Found reference field(s): J1427-4206
#2021-03-20 02:35:40 INFO fluxscale	 Found transfer field(s):  J1246-2547 J1305-2850
#2021-03-20 02:35:40 INFO fluxscale	 Flux density for J1246-2547 in SpW=0 (freq=2.21211e+11 Hz) is: 0.098105 +/- 0.00631426 (SNR = 15.5371, N = 90)
#2021-03-20 02:35:40 INFO fluxscale	 Flux density for J1246-2547 in SpW=1 (freq=2.24606e+11 Hz) is: 0.0974186 +/- 0.00630145 (SNR = 15.4597, N = 90)
#2021-03-20 02:35:40 INFO fluxscale	 Flux density for J1246-2547 in SpW=2 (freq=2.36411e+11 Hz) is: 0.0952679 +/- 0.00628222 (SNR = 15.1647, N = 90)
#2021-03-20 02:35:40 INFO fluxscale	 Flux density for J1246-2547 in SpW=3 (freq=2.39662e+11 Hz) is: 0.0948701 +/- 0.00626389 (SNR = 15.1456, N = 90)
#2021-03-20 02:35:40 INFO fluxscale	 Flux density for J1305-2850 in SpW=0 (freq=2.21211e+11 Hz) is: 0.00317594 +/- 0.000254571 (SNR = 12.4756, N = 90)
#2021-03-20 02:35:40 INFO fluxscale	 Flux density for J1305-2850 in SpW=1 (freq=2.24606e+11 Hz) is: 0.0031482 +/- 0.000238116 (SNR = 13.2213, N = 90)
#2021-03-20 02:35:40 INFO fluxscale	 Flux density for J1305-2850 in SpW=2 (freq=2.36411e+11 Hz) is: 0.0029976 +/- 0.000265412 (SNR = 11.2941, N = 90)
#2021-03-20 02:35:40 INFO fluxscale	 Flux density for J1305-2850 in SpW=3 (freq=2.39662e+11 Hz) is: 0.0029919 +/- 0.000317503 (SNR = 9.42323, N = 90)
#2021-03-20 02:35:40 INFO fluxscale	 Fitted spectrum for J1246-2547 with fitorder=1: Flux density = 0.0964057 +/- 4.07545e-05 (freq=230.342 GHz) spidx: a_1 (spectral index) =-0.423839 +/- 0.0125671 covariance matrix for the fit:  covar(0,0)=0.00106465 covar(0,1)=0.00164434 covar(1,0)=0.00164434 covar(1,1)=4.98836
#2021-03-20 02:35:40 INFO fluxscale	 Fitted spectrum for J1305-2850 with fitorder=1: Flux density = 0.00307658 +/- 7.33596e-06 (freq=230.342 GHz) spidx: a_1 (spectral index) =-0.821432 +/- 0.0724789 covariance matrix for the fit:  covar(0,0)=0.00191732 covar(0,1)=0.0288311 covar(1,0)=0.0288311 covar(1,1)=9.3923

#
#
applycal(vis= prefix + '_line.ms', flagbackup=False, field='', interp=['nearest','nearest', 'linear','nearest'], gainfield = '', gaintable=['B0','P0','P1', '.G0.flux'], spwmap=[[0,1,2,3], [0,1,2,3], [0,0,0,0], [0,1,2,3]])
#-------- Split into target source
os.system('rm -rf ' + BPCAL + '.ms'); split(vis=prefix + '_line.ms', outputvis=BPCAL+'.ms', field=BPCAL, datacolumn='corrected')
os.system('rm -rf ' + PHCAL + '.ms'); split(vis=prefix + '_line.ms', outputvis=PHCAL+'.ms', field=PHCAL, datacolumn='corrected')
os.system('rm -rf ' + CHECK + '.ms'); split(vis=prefix + '_line.ms', outputvis=CHECK+'.ms', field=CHECK, datacolumn='corrected')
os.system('rm -rf ' + TARGET + '.ms'); split(vis=prefix + '_line.ms', outputvis=TARGET+'.ms', field=TARGET, datacolumn='corrected')
#-------- Imaging calibrators
##---- Imaging J0423-0120
os.system('rm -rf SC.Gap0')
gaincal(vis=BPCAL+'.ms', caltable='SC.Gap0', spw='*', solint='int,inf', refant=REFANT, gaintype='G', smodel=[2.06031577678287, 0, 0, 0], calmode='ap', minblperant=5, minsnr=3)
plotcal(caltable = 'SC.Gap0', xaxis = 'time', yaxis = 'phase', plotsymbol='.', plotrange = [0,0,-20,20], iteration = 'antenna', figfile='SC.Gap0.phase.png', subplot = 221)
plotcal(caltable = 'SC.Gap0', xaxis = 'time', yaxis = 'amp', plotsymbol='.', plotrange = [0,0,0.0,2.0], iteration = 'antenna', figfile='SC.Gap0.amp.png', subplot = 221)
applycal(vis=BPCAL+'.ms', interp='nearest', gaintable='SC.Gap0', flagbackup=False)
os.system('rm -rf ' + BPCAL + '_SPW*')
tclean( vis=BPCAL+'.ms', imagename=BPCAL + '_SPW0', spw='0', specmode='cube', start=0, nchan=1920, width=1, niter=10000, threshold='0.000mJy', imsize=128, gain=0.1, cell='0.1arcsec', weighting='natural', interactive=True, pbcor=False)
tclean( vis=BPCAL+'.ms', imagename=BPCAL + '_SPW1', spw='1', specmode='cube', start=0, nchan=1920, width=1, niter=10000, threshold='0.000mJy', imsize=128, gain=0.1, cell='0.1arcsec', weighting='natural', interactive=True, pbcor=False)
tclean( vis=BPCAL+'.ms', imagename=BPCAL + '_SPW2', spw='2', specmode='cube', start=0, nchan=1920, width=1, niter=10000, threshold='0.000mJy', imsize=128, gain=0.1, cell='0.1arcsec', weighting='natural', interactive=True, pbcor=False)
tclean( vis=BPCAL+'.ms', imagename=BPCAL + '_SPW3', spw='3', specmode='cube', start=0, nchan=1920, width=1, niter=10000, threshold='0.000mJy', imsize=128, gain=0.1, cell='0.1arcsec', weighting='natural', interactive=True, pbcor=False)
##---- Imaging PhaseCal
os.system('rm -rf SC.Gap0')
gaincal(vis=PHCAL+'.ms', caltable='SC.Gap0', spw='*', solint='int,inf', refant=REFANT, gaintype='G', smodel=[0.096, 0, 0, 0], calmode='ap', minblperant=5, minsnr=3)
plotcal(caltable = 'SC.Gap0', xaxis = 'time', yaxis = 'phase', plotsymbol='.', plotrange = [0,0,-20,20], iteration = 'antenna', figfile='SC.Gap0.phase.png', subplot = 221)
plotcal(caltable = 'SC.Gap0', xaxis = 'time', yaxis = 'amp', plotsymbol='.', plotrange = [0,0,0.0,2.0], iteration = 'antenna', figfile='SC.Gap0.amp.png', subplot = 221)
applycal(vis=PHCAL+'.ms', interp='nearest', gaintable='SC.Gap0', flagbackup=False)
os.system('rm -rf ' + PHCAL + '_SPW*')
tclean( vis=PHCAL+'.ms', imagename=PHCAL + '_SPW0', spw='0', specmode='cube', start=0, nchan=1920, width=1, niter=10000, threshold='0.000mJy', imsize=128, gain=0.1, cell='0.1arcsec', weighting='natural', interactive=True, pbcor=False)
tclean( vis=PHCAL+'.ms', imagename=PHCAL + '_SPW1', spw='1', specmode='cube', start=0, nchan=1920, width=1, niter=10000, threshold='0.000mJy', imsize=128, gain=0.1, cell='0.1arcsec', weighting='natural', interactive=True, pbcor=False)
tclean( vis=PHCAL+'.ms', imagename=PHCAL + '_SPW2', spw='2', specmode='cube', start=0, nchan=1920, width=1, niter=10000, threshold='0.000mJy', imsize=128, gain=0.1, cell='0.1arcsec', weighting='natural', interactive=True, pbcor=False)
tclean( vis=PHCAL+'.ms', imagename=PHCAL + '_SPW3', spw='3', specmode='cube', start=0, nchan=1920, width=1, niter=10000, threshold='0.000mJy', imsize=128, gain=0.1, cell='0.1arcsec', weighting='natural', interactive=True, pbcor=False)
##---- Imaging Check
applycal(vis=CHECK+'.ms', interp='linear', gaintable='SC.Gap0', flagbackup=False)
os.system('rm -rf ' + CHECK + '_SPW*')
tclean( vis=CHECK+'.ms', imagename=CHECK + '_SPW0', spw='0', specmode='cube', start=0, nchan=1920, width=1, niter=10000, threshold='0.000mJy', imsize=128, gain=0.1, cell='0.1arcsec', weighting='natural', interactive=True, pbcor=False)
tclean( vis=CHECK+'.ms', imagename=CHECK + '_SPW1', spw='1', specmode='cube', start=0, nchan=1920, width=1, niter=10000, threshold='0.000mJy', imsize=128, gain=0.1, cell='0.1arcsec', weighting='natural', interactive=True, pbcor=False)
tclean( vis=CHECK+'.ms', imagename=CHECK + '_SPW2', spw='2', specmode='cube', start=0, nchan=1920, width=1, niter=10000, threshold='0.000mJy', imsize=128, gain=0.1, cell='0.1arcsec', weighting='natural', interactive=True, pbcor=False)
tclean( vis=CHECK+'.ms', imagename=CHECK + '_SPW3', spw='3', specmode='cube', start=0, nchan=1920, width=1, niter=10000, threshold='0.000mJy', imsize=128, gain=0.1, cell='0.1arcsec', weighting='natural', interactive=True, pbcor=False)
##---- Imaging Target
applycal(vis=TARGET+'.ms', interp='linear', gaintable='SC.Gap0', flagbackup=False)
os.system('rm -rf ' + TARGET + '_SPW*')
tclean( vis=TARGET+'.ms', imagename=TARGET + '_SPW0', spw='0', specmode='cube', start=0, nchan=1920, width=1, niter=100000, threshold='0.000mJy', imsize=256, gain=0.1, cell='0.1arcsec', weighting='natural', interactive=True, pbcor=False)
tclean( vis=TARGET+'.ms', imagename=TARGET + '_SPW1', spw='1', specmode='cube', start=0, nchan=1920, width=1, niter=100000, threshold='0.000mJy', imsize=256, gain=0.1, cell='0.1arcsec', weighting='natural', interactive=True, pbcor=False)
tclean( vis=TARGET+'.ms', imagename=TARGET + '_SPW2', spw='2', specmode='cube', start=0, nchan=1920, width=1, niter=10000, threshold='0.000mJy', imsize=256, gain=0.1, cell='0.1arcsec', weighting='natural', interactive=True, pbcor=False)
tclean( vis=TARGET+'.ms', imagename=TARGET + '_SPW3', spw='3', specmode='cube', start=0, nchan=1920, width=1, niter=10000, threshold='0.000mJy', imsize=256, gain=0.1, cell='0.1arcsec', weighting='natural', interactive=True, pbcor=False)
'''
