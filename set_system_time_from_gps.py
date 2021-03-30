from gps import *
import os

def get_gps_datetime (gpsd):
	nx = gpsd.next()
	
	if (nx['class'] == 'TPV'):
		gps_dtg = getattr(nx, 'time', "Unknown")
	
		if (gps_dtg != "Unknown"):
			#print("GPS time: %s" %(gps_dtg))
			return gps_dtg
		
		else:
			return None

if __name__ == '__main__':
	gpsd = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE)
	gps_dtg = None
	
	while (gps_dtg == None):
		gps_dtg = get_gps_datetime()
	
	date = gps_dtg[:10]
	time = gps_dtg[11:]
	dtg = '%s %s'%(date, time)

	os.system('sudo date +"%Y-%m-%d %R:%S" --set="' + dtg + '"')
	os.system('date')
	#print("%s" %(dtg))	# return the date if script is run as main
