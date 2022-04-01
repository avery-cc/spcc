import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from scipy.io import wavfile


def generate_specgram():
    """generates spectrogram from user input"""
    # ask for filename
    filename = 'hmpback1.wav' #input("Filename: ")
    # read in sample rate of wav file and numpy array
    sample_rate, signal_data = wavfile.read(filename)
    time = len(signal_data) / sample_rate

    fig, ax = plt.subplots()
    ax = plt.specgram(signal_data, Fs=sample_rate, cmap='Greys')
    plt.xlabel('Time')
    plt.ylabel('Frequency')

    # add space for slider
    plt.subplots_adjust(bottom=0.25)

    # adjust slider
    slider_color = "White"
    axis_position = plt.axes([0.2, 0.1, 0.65, 0.03],
                             facecolor=slider_color)
    slider_position = Slider(axis_position,
                             'Pos', 0.1, 90.0)

    def update(val):
        pos = slider_position.val
        ax.axis([pos, pos+10, -1, 1])
        fig.canvas.draw_idle()

    slider_position.on_changed(update)

    plt.show()


generate_specgram()
