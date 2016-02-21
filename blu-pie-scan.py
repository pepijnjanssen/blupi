#!/usr/bin/env python

import sys
import subprocess as sp
import time
from os import devnull

# Global variables until we have a config file
fmin = 151000000
fmax = 156500000
alarmthresh = 4
powerfftw_path = "/usr/local/bin/rtl_power_fftw"
fftbins = 512
otherargs = "-c"
block_scan_time = 0.75

# Parameter formatting
frange = str(fmin) + ":" + str(fmax)
frange = "-f " + frange
fftbins = "-b " + str(fftbins)
bstime = "-t " + str(block_scan_time)
dvnll = open(devnull, 'wb')

# Let's run this bitch!
if __name__ == '__main__':

	# Housekeeping:
	floats = []

	try:
		print "Starting up at", time.strftime("%H:%M:%S")
		
		# Insert baseline file generation subroutine here once main script is completed

		rtlscan = sp.Popen([powerfftw_path, frange, fftbins, otherargs, bstime], stdout=sp.PIPE, stderr=dvnll, shell=False)

		lines_iterator = iter(rtlscan.stdout.readline, b"")
		for line in lines_iterator:

			if '#' in line or not line.strip():
				floats = [0,-99]
			else:
				floats = map(float, line.split())

			if floats[1] >= alarmthresh:

				freq_temp = round(floats[0] /1000000, 3)
				print "At " + time.strftime("%H:%M:%S") + ", a " + str(round(floats[1], 1)) + " dB/Hz signal was detected at " + str(freq_temp) + " MHz."

	except (KeyboardInterrupt, SystemExit): # Press ctrl-c

		rtlscan.kill()
