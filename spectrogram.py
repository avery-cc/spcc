import matplotlib.pyplot as plt
from scipy.io import wavfile


def generate_specgram():
    """generates spectrogram from user input"""
    # ask for filename
    filename = 'hmpback1.wav' #input("Filename: ")
    # read in sample rate of wav file and numpy array
    sample_rate, signal_data = wavfile.read(filename)
    time = len(signal_data) / sample_rate
    plt.subplot()
    title = 'specgram' #input("Plot title: ")
    plt.title(title)

    plt.specgram(signal_data, Fs=sample_rate, cmap='Greys')
    plt.xlabel('Time')
    plt.ylabel('Frequency')

    plt.show()


generate_specgram()
