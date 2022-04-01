import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import RectangleSelector
from scipy.io import wavfile


def generate_specgram():
    """generates spectrogram from user input and clips selection"""
    # ask for filename
    filename = 'hmpback1.wav' #input("Filename: ")
    # read in sample rate of wav file and numpy array
    sample_rate, signal_data = wavfile.read(filename)
    time = len(signal_data) / sample_rate

    def line_select_callback(eclick, erelease):
        """display line selection and create new graph from selection"""
        time1, freq1 = eclick.xdata, eclick.ydata
        time2, freq2 = erelease.xdata, erelease.ydata
        print(f"({time1:3.2f}, {freq1:3.2f}) --> ({time2:3.2f}, {freq2:3.2f})")
        # create new data array
        new_data = []
        # extract sample number from selection
        time1_samples = int(time1 * sample_rate)
        time2_samples = int(time2 * sample_rate)
        # extract corresponding data from signal_data
        for sample in range(time1_samples, time2_samples):
            data_point_new = signal_data[sample]
            new_data.append(data_point_new)

        # display spectrogram of clipping
        plt.subplots()
        plt.title('Specgram clip')
        plt.specgram(new_data, Fs=sample_rate, cmap='Greys')
        plt.xlabel('Time')
        plt.ylabel('Frequency')
        plt.show()

        # save clip to txt file (CHANGE LOCATION???)
        clip_name = 'temp1' #input("Name of clip file: ")
        print("Close plots to continue")
        with open(clip_name, 'w') as f:
            for i in new_data:
                num = str(i)
                f.write(f"{num}\n")
            f.close()

    # display spectrogram of file
    fig, ax = plt.subplots()
    plt.title('specgram')  # input("Plot title: ")
    plt.specgram(signal_data, Fs=sample_rate, cmap='Greys')
    plt.xlabel('Time')
    plt.ylabel('Frequency')

    # drawtype is 'box' or 'line' or 'none'
    select_tool = RectangleSelector(ax, line_select_callback,
                                    drawtype='box', useblit=True,
                                    button=[1],  # use left click
                                    minspanx=5, minspany=5,
                                    spancoords='pixels',
                                    interactive=True)
    fig.canvas.mpl_connect('key_press_event', select_tool)
    plt.show()


def generate_template():
    """creates template array from template txt file"""
    temp_file = 'temp1' #input("Name of template file: ")
    with open(temp_file, 'r') as f:
        temp_list = []
        for line in f:
            num = int(line.strip())
            temp_list.append(num)
        f.close()
    temp_array = np.array(temp_list)
    return temp_array


def cross_correlate(whole_array, sub_array):
    """create array of whole file values similar to template array
    based on user specified threshold"""
    # input threshold cutoff value
    threshold = 20
    sub = sub_array
    whole = whole_array
    print(sub)
    print(whole)
    # create empty array for storage
    values = np.array([])
    coeffs_list = []
    whole_indices = []
    wholeindex = 0
    subindex = 0
    while subindex < len(sub) and wholeindex < len(whole):
        coeff_similarity = (sub[subindex] - whole[wholeindex])**2
        if coeff_similarity < threshold:
            # move to next data pair
            subindex += 1
            wholeindex += 1
            coeffs_list.append(coeff_similarity)
            whole_indices.append(wholeindex)
        else:
            subindex = 0
            wholeindex += 1
            whole_indices.clear()
            coeffs_list.clear()

    print(coeffs_list)
    print(whole_indices)
    plt.subplots()
    xvalues = []
    count = 0
    for i in coeffs_list:
        xvalues.append(count)
        count += 1
    yvalues = coeffs_list
    plt.plot(xvalues, yvalues)
    plt.show()
    return whole_indices


def create_new_template():
    """asks user to create new templates"""
    while True:
        choice = input("Do you want to create a new template? (y/n): ")
        if choice == 'y':
            generate_specgram()
            template = generate_template()
            print("Template created")
            return template
        elif choice == 'n':
            break


def get_signal_data(filename):
    """retrieves original signal data"""
    sample, signal_data = wavfile.read(filename)
    return signal_data


def plot_match(match_indices, filename):
    """plots spectrogram and highlights match index range"""
    # read in wav file
    sample_rate, signal_data = wavfile.read(filename)
    # time = len(signal_data) / sample_rate
    time1 = match_indices[0]
    time2 = match_indices[-1]
    # plot spectrogram
    plt.subplots()
    plt.title('specgram')  # input("Plot title: ")
    plt.axvspan(time1, time2, color='red', alpha=0.5)
    plt.specgram(signal_data, Fs=sample_rate, cmap='Greys')
    plt.xlabel('Time')
    plt.ylabel('Frequency')


plot_match(cross_correlate(get_signal_data('hmpback1.wav'), create_new_template()), 'hmpback1.wav')
