import matplotlib
import seaborn
import math.sine


Fs = 10000000     # Sampling frequency                    
T = 1/Fs          # Sampling period       
L = 1200          # Length of signal
t = (0:L-1)*T     # Time vector
freq = 1420000000

signal = 0.7*sine(2*pi*freq*t)

corrupted_signal = signal + 2*rand(size(t))

fig, ((ax1, ax2, ax3, ax4)) = plt.subplots(nrows = 4, ncols=1, sharex=True)







ax1 = plt.gca()










def plot_Cycle(CycleDataSet):
    df = CycleDataSet.DataFrame
    Info500 = CycleDataSet.DataSetDict
    fig, ((ax1, ax2, ax3, ax4, ax5)) = plt.subplots(nrows=5, ncols=1, sharex=True)  # ,sharey=True,figsize=(10,5))
    cycleTime = list(Info500["CorrectedTimes"])

    tempList = list(Info500["resistBP1List"])
    for item in tempList:
        df.iloc[:, item].plot(x=cycleTime, y=df.iloc[:, item], ylim=(0, 90), ax=ax1)
    ax1 = plt.gca()
    # ax1.set_title("Resistors: BackPlane 1")

    tempList = list(Info500["resistBP2List"])
    for item in tempList:
        df.iloc[:, item].plot(x=cycleTime, y=df.iloc[:, item], ylim=(0, 1.6), ax=ax2)
    ax2 = plt.gca()
    # ax2.set_title("Resistors: BackPlane 2")

    tempList = list(Info500["capBP1List"])
    for item in tempList:
        df.iloc[:, item].plot(x=cycleTime, y=df.iloc[:, item], ax=ax3)
    ax3 = plt.gca()
    # ax3.set_title("Capacitors: BackPlane 1")

    tempList = list(Info500["capBP2List"])
    for item in tempList:
        df.iloc[:, item].plot(x=cycleTime, y=df.iloc[:, item], ax=ax4)
    ax4 = plt.gca()
    # ax4.set_title("Capacitors: BackPlane 2")

    tempList = list(Info500["resistMUXList"])
    for item in tempList:
        df.iloc[:, item].plot(x=cycleTime, y=df.iloc[:, item], ax=ax5)
    ax5 = plt.gca()
    # ax5.set_title("Resistors: MUX")




plot(1000*t(1:50),X(1:50))
title('Signal Corrupted with Zero-Mean Random Noise')
xlabel('t (milliseconds)')
ylabel('X(t)')

Y = fft(X);

P2 = abs(Y/L);
P1 = P2(1:L/2+1);
P1(2:end-1) = 2*P1(2:end-1);

f = Fs*(0:(L/2))/L;
plot(f,P1) 
title('Single-Sided Amplitude Spectrum of X(t)')
xlabel('f (Hz)')
ylabel('|P1(f)|')

Y = fft(S);
P2 = abs(Y/L);
P1 = P2(1:L/2+1);
P1(2:end-1) = 2*P1(2:end-1);

plot(f,P1) 
title('Single-Sided Amplitude Spectrum of S(t)')
xlabel('f (Hz)')
ylabel('|P1(f)|')
