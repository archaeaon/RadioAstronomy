import sys
import math
import SoapySDR
from SoapySDR import *  # SOAPY_SDR_ constants
import numpy as np # use numpy for buffers
import time
import gps_dtg
from datetime import datetime, timedelta

def FindDevice():
	# enumerate devices
	results = SoapySDR.Device.enumerate()
	print("Devices Found: ")
	for result in results: print(result)

	# create device instance
	# args can be user defined or from the enumeration result
	args = dict(driver="lime")
	#args = results[0]
	print("Instantiating device: ")
	return SoapySDR.Device(args)


def QueryDevice(sdr, chan):
	#print("Possible Antennas: " + str(sdr.listAntennas(SOAPY_SDR_RX, 0)))

	# query device info
	print("Antennas: " + str(sdr.listAntennas(SOAPY_SDR_RX, 0)))
	print("Gains: " + str(sdr.listGains(SOAPY_SDR_RX, 0)))
	print("Frequency Range: ")
	freqs = sdr.getFrequencyRange(SOAPY_SDR_RX, 0)
	for freqRange in freqs: print(freqRange)


def ConfigureDevice(sdr, MasterClockRate=30.72e6):
	#sdr.setMasterClockRate(MasterClockRate)
	print("Actual Master Clock Rate %f Msps" % (sdr.getMasterClockRate() / 1e6))


def ConfigureRX(sdr, chan, RX_SampleRate=None, CenterFrequency=None, RX_Antenna=None, RX_Gain=None,
		        RX_FrequencyOffset=None):
	if RX_SampleRate is not None:
		print("Setting RX sample rate to %g" % RX_SampleRate)
		sdr.setSampleRate(SOAPY_SDR_RX, chan[0], RX_SampleRate)
		sdr.setSampleRate(SOAPY_SDR_RX, chan[1], RX_SampleRate)
		print("Actual Rx Rate %f Msps" % (sdr.getSampleRate(SOAPY_SDR_RX, chan[0]) / 1e6))

	if CenterFrequency is not None:
		print("Setting RX frequency to %g" % CenterFrequency)
		sdr.setFrequency(SOAPY_SDR_RX, chan[0], CenterFrequency)
		sdr.setFrequency(SOAPY_SDR_RX, chan[1], CenterFrequency)
		print("Actual Rx Freq %f MHz" % (sdr.getFrequency(SOAPY_SDR_RX, chan[0]) / 1e6))

	if RX_Antenna is not None:
		print("Setting RX antenna to " + str(RX_Antenna))
		sdr.setAntenna(SOAPY_SDR_RX, chan[0], RX_Antenna)
		sdr.setAntenna(SOAPY_SDR_RX, chan[1], RX_Antenna)
		print("Antenna on Channel %i is %s" % (chan[0], sdr.getAntenna(SOAPY_SDR_RX, chan[0])))
		print("Antenna on Channel %i is %s" % (chan[1], sdr.getAntenna(SOAPY_SDR_RX, chan[1])))

	if RX_Gain is not None:
		print("Setting RX gain to " + str(RX_Gain))
		sdr.setGain(SOAPY_SDR_RX, chan[0], RX_Gain)  ###TODO::Is LNA the Default?????
		sdr.setGain(SOAPY_SDR_RX, chan[1], RX_Gain)
		print("Actual Rx Gain %f " % (sdr.getGain(SOAPY_SDR_RX, chan[0])))
		# sdr.setGain(SOAPY_SDR_RX, 0, "TIA", 5.0)
		# sdr.setGain(SOAPY_SDR_RX, 0, "PGA", 5.0)
		# sdr.setGain(SOAPY_SDR_RX, 0, "LNA", 35.0)

	# #set dc offset mode to False to disable automatic DC bias removal
	# sdr.setDCOffsetMode(SOAPY_SDR_RX, chan, False)
	# print("Getting RX DC offset mode: " + str(sdr.getDCOffsetMode(SOAPY_SDR_RX, 0)))
	# print("Getting RX DC offset: " + str(sdr.getDCOffset(SOAPY_SDR_RX, 0)))
	# sdr.setBandwidth(SOAPY_SDR_RX, chan, 5e6)
	# print("Getting RX bandwidth: " + str(sdr.getBandwidth(SOAPY_SDR_RX, 0)))

	# sdr.testSignalDC(0x3fff, 0x3fff)

	time.sleep(1)


def StartRX(sdr, chan):
	# setup a stream (complex floats)
	print("Setting up RX stream")
	args = dict(skipCal="false")
	# return sdr.setupStream(SOAPY_SDR_RX, SOAPY_SDR_CF32, chan, args)
	return sdr.setupStream(SOAPY_SDR_RX, SOAPY_SDR_CS16, chan)


def RunRX(sdr, rxStream, samplerate, freq, time):
	###################################################
	# create a re-usable buffer for rx samples
	"""buff = np.array([0] * 2040,
		            np.complex64)
	sdr.activateStream(rxStream, SOAPY_SDR_END_BURST, 0, buff.size)

	# Receive samples, find pilot tone, put in neural network queue.
	totalRead = 0;
	while True:

		# Read from the stream (is this thread/multiprocess safe?).
		sr = sdr.readStream(rxStream, [buff], len(buff), timeoutUs=int(5e5))
		print("Number rx samples {}".format(sr.ret))  # num samples or error code

		if sr.ret == -1:
		    break

		totalRead += sr.ret

	print("Total samples read {}".format(totalRead))"""
	###################################################
	# # create a re-usable buffer for rx samples
	"""buff = np.array([0] * 1024, np.complex64)
	
	sdr.activateStream(rxStream, SOAPY_SDR_END_BURST, 0, buff.size)
	
	# receive some samples
	for i in range(10):
		sr = sdr.readStream(rxStream, [buff], len(buff))
		print(sr.ret)  # num samples or error code
		print(sr.flags)  # flags set by receive operation
		print(sr.timeNs)  # timestamp for receive buffer"""


####################################
# # Read samples into this buffer
# num_samps = 2 ** 14  # 16384 samples
# sampsRx = [np.zeros(num_samps, numpy.complex64), numpy.zeros(num_samps, numpy.complex64)]
# buff0 = sampsRx[0]  # RF Chain A
# buff1 = sampsRx[1]  # RF Chain B
# sdr.activateStream(rxStream,  # stream object
#		            SOAPY_SDR_END_BURST,  # flags
#		            0,  # timeNs (don't care unless using SOAPY_SDR_HAS_TIME)
#		            buff0.size)  # numElems - this is the burst size
# sr = sdr.readStream(rxStream, [buff0, buff1], buff0.size)
################################################
	print('===== receive a continuous stream =====')
	sdr.activateStream(rxStream)
	
	buff0 = np.zeros(2 * samplerate, np.int32)
	buff1 = np.zeros(2 * samplerate, np.int32)
	
	print('readStream continuously...')
	#doneLoopTime = time.time() + 0.1
	#while time.time() < doneLoopTime:
	num_elements = 2 * samplerate
	while num_elements > 0:
		sr = sdr.readStream(rxStream, [buff0, buff1], 2 * samplerate)
		#sr = sdr.readStream(rxStream, [buff0], 2*samplerate)
		num_elements -= sr.ret
	
	sdr.deactivateStream(rxStream)
	#print(buff0[samplerate - 10: samplerate + 10])
	#print('readStream for a timeout...')
	#sr = sdr.readStream(rxStream, [buff0, buff1], 1024)
	print(sr)
	#print(sr.flags)

	#np.savetxt('limesdr_test_data_at_%.2eGHz.txt'%(freq), buff0.view(float).reshape(-1,2))
	np.savetxt(sys.argv[1] + time + '_%.2eGHz_chanA.txt'%(freq), buff0.view(int).reshape(-1,1))	#TODO: Change filepath
	np.savetxt(sys.argv[1] + time + '_%.2eGHz_chanB.txt'%(freq), buff1.view(int).reshape(-1,1))	#TODO: Change filepath
	
	#S = np.fft.fftshift(np.fft.fft(buff0, samplerate) / samplerate)
	
	#plt.figure(num=1)
	#plt.subplot(211)
	#t_us = np.arrange(N) / fs / 1e-6
	#plt.plot(t_us, buff0.real, 'k', label='I')
	#plt.plot(t_us, buff0.imag, 'r', label='Q')
	#plt.xlim(t_us[0], t_us[-1])
###################################################
# # start streaming
# sdr.activateStream(rxStream, 0, 0, numSamps)
#
# # buffer for storing accumulated samples
# rxBuffs = np.array([], np.complex64)
# # create a re-usable buffer for rx samples
# rxBuff = np.array([0] * burstSize, np.complex64)
#
# # receive some samples
# while True:
#	 sr = sdr.readStream(rxStream, [rxBuff], len(rxBuff))
#	 print(sr.ret)  # num samples or error code
#
#	 # stash time on first buffer
#	 if sr.ret > 0 and len(rxBuffs) == 0:
#		 rxTime0 = sr.timeNs
#		 if (sr.flags & SOAPY_SDR_HAS_TIME) == 0:
#		     raise Exception('receive fail - no timestamp on first readStream %s' % (str(sr)))
#
#	 # accumulate buffer or exit loop
#	 if sr.ret > 0:
#		 rxBuffs = np.concatenate((rxBuffs, rxBuff[:sr.ret]))
#	 else:
#		 break
#
# # process data
# print
# len(rxBuffs)
# print("Captured %i samples in total" % (len(rxBuffs)))
# print
# np.real(rxBuffs[10000]), np.real(rxBuffs[10001]), np.real(rxBuffs[10002])
# dump samples
# np.savetxt('outfile.txt', rxBuffs,'%.10f\t%.10f')
###################################################
###################################################
###################################################
###################################################


def CloseRX(sdr, rxStream):
	print("Deactivating RX stream")
	sdr.deactivateStream(rxStream)  # stop streaming
	print("Closing RX stream")
	sdr.closeStream(rxStream)


def ConfigureTX(sdr):
	pass


def StartTX(sdr):
	pass


def CloseTX(sdr):
	pass


if __name__ == '__main__':
	### Desired Parameters ###
	dtg1 = datetime.strptime("1 Jan 1970", "%d %b %Y")	#set to the epoch
	dtg2 = datetime.strptime("1 Jan 1970", "%d %b %Y")	#set to the epoch
	chan = [0,1]
	antenna = "LNAW"
	samplerate = 30e6
	frequency = 1.42e9
	#frequency = float(sys.argv[1])	# Arg 1 is now obsolete. Update if you wish to use this.
	gain = 20
	##########################

	sdr = FindDevice()
	QueryDevice(sdr, chan)

	ConfigureDevice(sdr)
	ConfigureRX(sdr, chan, RX_Antenna=antenna, RX_SampleRate=samplerate, CenterFrequency=frequency, RX_Gain=gain)

	#try:
	while True:		# run until manual termination or shutdown
		time, dtg2 = gps_dtg.get_time()
		dtg2 = datetime.strptime(dtg2, "%b%d%Y %M:%H:%S")	#TODO: Check this how the dtg is formatted directly from the GPS

		if (dtg2 >= dtg1 + timedelta(minutes=10)):		# if it's been 10 minutes since the last time data was collected, collect more data
			rxStream = StartRX(sdr, chan)
			time, dtg2 = gps_dtg.get_time() #TODO: Get the time from GPS
			RunRX(sdr, rxStream, int(samplerate), frequency, time)
			CloseRX(sdr, rxStream)
			dtg2 = datetime.strptime(dtg2, "%b%d%Y %M:%H:%S")
			dtg1 = dtg2
"""
	except KeyboardInterrupt:
		try:
			sys.exit(0)

		except:
			os._exit(0)
"""
# # start streaming
# sdr.activateStream(rxStream, 0, 0, numSamps)
#
# # buffer for storing accumulated samples
# rxBuffs = np.array([], np.complex64)
# # create a re-usable buffer for rx samples
# rxBuff = np.array([0] * burstSize, np.complex64)
#
# # receive some samples
# while True:
#	 sr = sdr.readStream(rxStream, [rxBuff], len(rxBuff))
#	 print(sr.ret)  # num samples or error code
#
#	 # stash time on first buffer
#	 if sr.ret > 0 and len(rxBuffs) == 0:
#		 rxTime0 = sr.timeNs
#		 if (sr.flags & SOAPY_SDR_HAS_TIME) == 0:
#		     raise Exception('receive fail - no timestamp on first readStream %s' % (str(sr)))
#
#	 # accumulate buffer or exit loop
#	 if sr.ret > 0:
#		 rxBuffs = np.concatenate((rxBuffs, rxBuff[:sr.ret]))
#	 else:
#		 break

# # cleanup streams
# print("Cleanup streams")
# sdr.deactivateStream(rxStream)  # stop streaming
# sdr.closeStream(rxStream)

# # process data
# print
# len(rxBuffs)
# print("Captured %i samples in total" % (len(rxBuffs)))
# print
# np.real(rxBuffs[10000]), np.real(rxBuffs[10001]), np.real(rxBuffs[10002])
# # dump samples
# # np.savetxt('outfile.txt', rxBuffs,'%.10f\t%.10f')


# # receive slightly before transmit time
# rx_buffs = np.array([], np.complex64)
# rx_flags = SOAPY_SDR_HAS_TIME | SOAPY_SDR_END_BURST
# # half of the samples come before the transmit time
# receive_time = int(tx_time_0 - (num_rx_samps / rate) * 1e9 / 2)
# sdr.activateStream(rx_stream, rx_flags, receive_time, num_rx_samps)
# rx_time_0 = None
#
# # accumulate receive buffer into large contiguous buffer
# while True:
#	 rx_buff = np.array([0] * 1024, np.complex64)
#	 timeout_us = int(5e5)  # 500 ms >> stream time
#	 status = sdr.readStream(rx_stream, [rx_buff], len(rx_buff), timeoutUs=timeout_us)
#
#	 # stash time on first buffer
#	 if status.ret > 0 and rx_buffs.size == 0:
#		 rx_time_0 = status.timeNs
#		 if (status.flags & SOAPY_SDR_HAS_TIME) == 0:
#		     raise Exception('receive fail - no timestamp on first readStream %s' % (str(status)))
#
#	 # accumulate buffer or exit loop
#	 if status.ret > 0:
#		 rx_buffs = np.concatenate((rx_buffs, rx_buff[:status.ret]))
#	 else:
#		 break

# # check resulting buffer
# if len(rx_buffs) != num_rx_samps:
#	 raise Exception(
#		 'receive fail - captured samples %d out of %d' % (len(rx_buffs), num_rx_samps))
# if rx_time_0 is None:
#	 raise Exception('receive fail - no valid timestamp')

# # clear initial samples because transients
# rx_mean = np.mean(rx_buffs)
# for i in range(len(rx_buffs) // 100):
#	 rx_buffs[i] = rx_mean
#
#
# # normalize the samples
# def normalize(samps):
#	 samps = samps - np.mean(samps)  # remove dc
#	 samps = np.absolute(samps)  # magnitude
#	 samps = samps / max(samps)  # norm ampl to peak
#	 # print samps[:100]
#	 return samps

# # dump debug samples
# if dump_dir is not None:
#	 np.save(os.path.join(dump_dir, 'txNorm.npy'), tx_pulse_norm)
#	 np.save(os.path.join(dump_dir, 'rxNorm.npy'), rx_buffs_norm)
#	 np.save(os.path.join(dump_dir, 'rxRawI.npy'), np.real(rx_buffs))
#	 np.save(os.path.join(dump_dir, 'rxRawQ.npy'), np.imag(rx_buffs))
