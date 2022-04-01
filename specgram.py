import matplotlib.pyplot as plt
import scipy.signal
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
        clip_name = input("Name of clip file: ")
        print("Close plots to continue")
        with open(clip_name, 'w') as f:
            for i in new_data:
                num = str(i)
                f.write(f"{num}\n")
            f.close()

    def toggle_selector(event):
        print(' Key pressed.')
        if event.key == 't':
            if toggle_selector.RS.active:
                print(' RectangleSelector deactivated.')
                toggle_selector.RS.set_active(False)
            else:
                print(' RectangleSelector activated.')
                toggle_selector.RS.set_active(True)

    # display spectrogram of file
    fig, ax = plt.subplots()
    plt.title('specgram')  # input("Plot title: ")
    plt.specgram(signal_data, Fs=sample_rate, cmap='Greys')
    plt.xlabel('Time')
    plt.ylabel('Frequency')

    # drawtype is 'box' or 'line' or 'none'
    toggle_selector.RS = RectangleSelector(ax, line_select_callback,
                                           drawtype='box', useblit=True,
                                           button=[1],  # use left click
                                           minspanx=5, minspany=5,
                                           spancoords='pixels',
                                           interactive=True)
    fig.canvas.mpl_connect('key_press_event', toggle_selector)
    plt.show()


def generate_template():
    """creates template array from template txt file"""
    temp_file = input("Name of template file: ")
    with open(temp_file, 'r') as f:
        temp_list = []
        for line in f:
            num = int(line.strip())
            temp_list.append(num)
        f.close()
    temp_array = np.array(temp_list)
    return temp_array


def cross_correlate(array1, array2):
    """creates array correlating two n-dimensional arrays"""
    # correlates arrays
    # NOT RIGHT METHOD
    correlation = scipy.signal.correlate(array1, array2, mode='valid')
    print(correlation)
    # create correlation plot
    plt.subplot()
    plt.plot(correlation)
    plt.show()


def create_new_template():
    """asks user to create new templates"""
    while True:
        choice = input("Do you want to create a new template? (y/n): ")
        if choice == 'y':
            generate_specgram()
            generate_template()
            print("Template created")
        elif choice == 'n':
            break


def get_signal_data(filename):
    """retrieves original signal data"""
    sample, signal_data = wavfile.read(filename)
    return signal_data


cross_correlate(create_new_template(), get_signal_data('hmpback1.wav'))
