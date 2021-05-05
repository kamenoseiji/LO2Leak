library(knitr)
SPLogFile <- '/Users/skameno/Projects/LO2leakage/LO2Spur.log'
SP <- read.table(SPLogFile, header=T)
SP <- SP[order(SP$UID),]
SPtable <- data.frame(Link=sprintf('[%s](http://www.alma.cl/~skameno/images/SP_%s_%s_SPW%d_POL-%s.pdf)', SP$UID, SP$UID, SP$Ant, SP$SPW, SP$POL), Ant=SP$Ant, SPW=SP$SPW, Freq=SP$Freq, POL=SP$POL, SNR=SP$SNR )
SPJIRA <- data.frame(Link=sprintf('[%s|http://www.alma.cl/~skameno/images/SP_%s_%s_SPW%d_POL-%s.pdf]', SP$UID, SP$UID, SP$Ant, SP$SPW, SP$POL), Ant=SP$Ant, SPW=SP$SPW, Freq=SP$Freq, POL=SP$POL, SNR=SP$SNR )
#print(kable(SPtable, format = "markdown"))
print(kable(SPJIRA, format = "markdown"))