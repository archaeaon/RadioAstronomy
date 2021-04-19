# NOTE: This file was used in a previous iteration of our project's software.
#	It is currently unused and has been replaced by set_system_time_from_gps.py.
#	This file is only kept in case the functions in it might be needed in the future.

from gps import *

def get_gps_datetime (gpsd):
	nx = gpsd.next()
	
	if (nx['class'] == 'TPV'):
		gps_dtg = getattr(nx, 'time', "Unknown")
	
		if (gps_dtg != "Unknown"):
			#print("GPS time: %s" %(_gps_dtg))
			return gps_dtg
		
		else:
			return None

def get_time ():
	gpsd = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE)
	gps_dtg = None
	
	while (gps_dtg == None):			# this might not be necessary since this function should never be called before
		gps_dtg = get_gps_datetime(gpsd)	# the date is retrieved
	
	date = gps_dtg[:10]
	time = gps_dtg[11:]
	dtg = '%s %s'%(date, time)
	
	#print("%s" %(time))
	#print("%s" %(dtg))
	return time, dtg	# return the time and datetime if called from another script

def get_date ():
	gpsd = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE)
	gps_dtg = None
	
	while (gps_dtg == None):
		gps_dtg = get_gps_datetime(gpsd)
	
	date = gps_dtg[:10]
	
	return date

if __name__ == '__main__':
	date = get_date()
	print("%s" %(date))	# return the date if script is run as main
