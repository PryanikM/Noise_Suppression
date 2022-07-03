from scipy.io import wavfile
from scipy.fft import rfft, rfftfreq, irfft
import numpy as np
import copy


class NoiseSuppression:
    def __init__(self):
        self.__sample_rate = None
        self.__data = None
        self.__duration = None
        self.__normalized_tone = None
        self.__N = 0

        self.__yf = None
        self.__xf = None

        self.__new_yf = None

        self.__points_per_freq = None

        self.__newData = None

    def set_audio(self, path_to_audio='', data=None, sample_rate=None):
        if data is None and sample_rate is None:
            self.__sample_rate, self.__data = wavfile.read(path_to_audio)
            self.__data = self.__data.T
        self.__duration = self.__data.shape[0] / self.__sample_rate
        self.__normalized_tone = self.__data / 32768
        self.__N = int(self.__sample_rate * self.__duration)
        self.__xf = None

    def __make_frequency_response(self):
        self.__yf = rfft(self.__normalized_tone)
        self.__xf = rfftfreq(self.__N, 1 / self.__sample_rate)
        self.__points_per_freq = len(self.__xf) / (self.__sample_rate / 2)

    def get_frequency_response(self):
        if self.__xf is None:
            self.__make_frequency_response()
        return self.__xf, np.abs(self.__yf)

    def delete_noise(self):
        self.__new_yf = copy.deepcopy(self.__yf)
        target_idx = int(self.__points_per_freq * 4000)
        self.__new_yf[target_idx:] = 0
        return self.__xf, np.abs(self.__new_yf)

    def set_new_audio(self):
        self.__yf = copy.deepcopy(self.__new_yf)
        self.__data = irfft(self.__yf)

    def get_audio(self):
        return self.__data


import matplotlib.pyplot as plt

# n = NoiseSuppression()
# n.set_audio('C:/Project/USATU_Lab/Практика/music.wav')
# xf, yf = n.get_frequency_response()
# plt.plot(xf, yf)
# plt.show()
# xf, yf = n.delete_noise()
# plt.plot(xf, yf)
# plt.show()

