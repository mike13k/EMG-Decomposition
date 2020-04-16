import numpy as np
import matplotlib.pyplot as plt

def read_file(file_name):
    lines = [line.rstrip('\n') for line in open(file_name)]
    return np.array(lines).astype(np.float)

def emg_decompostion(original_signal, moving_avg):
    signal = np.copy(original_signal)

    # Rectify signal (absloute value)
    signal_after_rectify = np.copy(signal)
    signal_after_rectify[np.where(signal_after_rectify < 0)] = signal[np.where(signal < 0)] * -1

    # Set threshold
    threshold = 3 * np.std(signal_after_rectify[0:123])
    # print(threshold)

    # Moving Average
    signalTemp = np.zeros(signal.shape)
    for i in range(moving_avg,signal.shape[0]):
        signalTemp[i] = np.sum(signal_after_rectify[i-moving_avg+1:i+1]) / moving_avg
    signal_after_average = np.copy(signalTemp)

    # Detect MUAP
    doSkip = False
    muTemplates = []
    muapTimestamps = []
    muapClasses = []
    
    detection_signal = np.zeros(signal.shape)
    for i in range(0,signal.shape[0]):
        # Skip detection checking when still in the range of the previous MUAP (wait till signal is less than threshold)
        if doSkip:
            if signal_after_average[i] > threshold:
                continue
            else:
                doSkip = False
                
        tmp = np.copy(signal_after_average[i:i+moving_avg])
        isMUAP = all(tmp > threshold)
        if(isMUAP):
            muapTimestamps.append(i)
            detection_signal[i] = signal[i]
            
            peak_index = np.where(signal[i:i+moving_avg] == np.max(signal[i:i+moving_avg]))[0][0]
            peak_shift = peak_index - int(moving_avg / 2)
            tmp = np.copy(signal[i+peak_shift:i+moving_avg+peak_shift])

            if (len(muTemplates) == 0):
                muTemplates.append(tmp)
                muapClasses.append(0)
            else:
                classified = False
                D = 12.65 ** 5
                for j in range(len(muTemplates)):
                    currTemplate = np.copy(muTemplates[j])
                    pre_D = D
                    D = np.sum((tmp - currTemplate) ** 2)
                    if(D < (12 ** 5) and D < pre_D):
                        template_index = j
                        classified = True
                
                if(classified):
                    currTemplate = np.copy(muTemplates[template_index])                
                    muapClasses.append(template_index)
                    currTemplate = (currTemplate + tmp)/2
                    muTemplates[template_index] = np.copy(currTemplate)  #Update the template   
                else:  #create a new template in muTemplates
                    muapClasses.append(len(muTemplates))
                    muTemplates.append(tmp)
            
            if signal_after_average[i] > threshold:
                doSkip = True
        
    # muapPeaks = []
    # for i in range(len(muapTimestamps)):
    #     max = signal[muapTimestamps[i]]
    #     maxIndex = muapTimestamps[i]
    #     for j in range(muapTimestamps[i], muapTimestamps[i]+moving_avg):
    #         if(signal[j] > max):
    #             max = signal[j]
    #             maxIndex = j
    #     muapPeaks.append(maxIndex)

    return detection_signal, signal_after_average, signal_after_rectify, np.array(muapTimestamps), muTemplates, np.array(muapClasses)


original_signal = read_file('Data.txt')
detection_signal, signal_avg, signal_rectify, timestamps, templates, classes = emg_decompostion(original_signal,20)
start = 30000
end = 35000

# Draw Templates
fig, x = plt.subplots(1,len(templates))
for i in range(len(templates)):
    x[i].plot(templates[i])
plt.show()

# Draw detections
plt.plot(original_signal[start:end])
timestamps = timestamps[np.where(timestamps >= start)]
timestamps = timestamps[np.where(timestamps <= end)]
# print(len(timestamps))
classes = classes[np.where(timestamps >= start)]
classes = classes[np.where(timestamps <= end)]
for i in range(len(templates)):
    # plt.plot(timestamps[np.where(classes == i)[0]], np.ones(timestamps[np.where(classes == i)[0]].shape) * 900, "*")
    plt.plot(timestamps[np.where(classes == i)[0]] - start, np.ones(timestamps[np.where(classes == i)[0]].shape) *
    900,
    # original_signal[timestamps[np.where(classes == i)[0]]],
    "*")
plt.show()


# # Extra
# fig, x = plt.subplots(4,1)
# x[0].plot(original_signal[start:end])
# x[0].title.set_text("Original Signal")
# x[1].plot(signal_rectify)
# # x[1].plot(signal_rectify[start:end])
# x[1].title.set_text("Rectify")
# x[2].plot(signal_avg)
# # x[2].plot(signal_avg[start:end])
# x[2].title.set_text("Moving Average")
# x[3].plot(detection_signal)
# # x[3].plot(detection_signal[start:end])
# x[3].title.set_text("Det")
# plt.show()
