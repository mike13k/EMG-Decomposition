import numpy as np
import matplotlib.pyplot as plt

def read_file(file_name):
    lines = [line.rstrip('\n') for line in open(file_name)]
    return np.array(lines).astype(np.float)

def emg_decompostion(original_signal, moving_avg):
    signal = np.copy(original_signal)

    # Rectify signal (absloute value)
    signal[np.where(signal < 0)] = signal[np.where(signal < 0)] * -1

    signal_after_rectify = np.copy(signal)

    # Set threshold
    threshold = 3 * np.std(signal[0:285])

    # Moving Average
    signalTemp = np.zeros(signal.shape)
    for i in range(moving_avg,signal.shape[0]):
        signalTemp[i] = np.sum(signal[i-moving_avg+1:i+1]) / moving_avg
    signal = signalTemp

    signal_after_average = np.copy(signal)

    # Detect MUAP
    doSkip = False
    muTemplates = []
    muapTimestamps = []
    muapClasses = []
                  
    for i in range(0,signal.shape[0]):
        # Skip detection checking when still in the range of the previous MUAP (wait till signal is less than threshold)
        if doSkip:
            if signal[i] > threshold:
                continue
            else:
                doSkip = False
                
        tmp = signal[i:i+moving_avg+1] 
        isMUAP = all(tmp > threshold)
        if(isMUAP):
            muapTimestamps.append(i)

            if (len(muTemplates) == 0):
                muTemplates.append(tmp)
                muapClasses.append(0)
            else:
                classified = False
                for j in range(len(muTemplates)):
                    currTemplate = np.copy(muTemplates[j])
                    D = np.sum((tmp - currTemplate) ** 2)
                    if(D < (12.65 ** 5)):
                        muapClasses.append(j)
                        classified = True
                        currTemplate = (currTemplate + tmp)/2
                        muTemplates[j] = currTemplate  #Update the template
                        break
                        
                if(not(classified)):  #create a new template in muTemplates
                    muapClasses.append(len(muTemplates))
                    muTemplates.append(tmp)
                    
            
            i += moving_avg
            if signal[i] > threshold:
                doSkip = True
        



    return signal, signal_after_average, signal_after_rectify, muapTimestamps, muTemplates

original_signal = read_file('Data.txt')
emg, signal_avg, signal_rectify, timestamps, templates = emg_decompostion(original_signal,20)
# plt.plot(original_signal)
# plt.show()

fig, x = plt.subplots(len(templates),1)
for i in range(len(templates)):
    x[i].plot(templates[i])
plt.show()

#fig, x = plt.subplots(4,1)
#x[0].plot(original_signal[30000:35000])
#x[0].title.set_text("Original Signal")
#x[1].plot(signal_rectify[30000:35000])
#x[1].title.set_text("Rectify")
#x[2].plot(signal_avg[30000:35000])
#x[2].title.set_text("Moving Average")
#x[3].plot(detected_signal[30000:35000])
#x[3].title.set_text("Det")
#plt.show()

# fig, x = plt.subplots(4,1)
# x[0].plot(original_signal[0:2000])
# x[0].title.set_text("Original Signal")
# x[1].plot(signal_rectify[0:2000])
# x[1].title.set_text("Rectify")
# x[2].plot(signal_avg[0:2000])
# x[2].title.set_text("Moving Average")
# x[3].plot(detected_signal[0:2000])
# x[3].title.set_text("Detected")
# plt.show()

# fig, x = plt.subplots(4,1)
# x[0].plot(original_signal)
# x[0].title.set_text("Original Signal")
# x[1].plot(signal_rectify)
# x[1].title.set_text("Rectify")
# x[2].plot(signal_avg)
# x[2].title.set_text("Moving Average")
# x[3].plot(detected_signal)
# x[3].title.set_text("Detected")
# plt.show()