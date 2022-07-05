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
            try:
                self.__sample_rate, self.__data = wavfile.read(path_to_audio)
                self.__data = self.__data.T
            except Exception:
                return 0

        self.__normalized_tone = self.__data / 32768

        self.__duration = self.__data.shape[0] / self.__sample_rate
        self.__normalized_tone = self.__data / 32768
        self.__N = int(self.__sample_rate * self.__duration)
        self.__xf = None
        return 1

    def __make_frequency_response(self):
        self.__yf = rfft(self.__normalized_tone)
        self.__xf = rfftfreq(self.__N, 1 / self.__sample_rate)
        self.__points_per_freq = len(self.__xf) / (self.__sample_rate / 2)

    def get_frequency_response(self):
        if self.__xf is None:
            self.__make_frequency_response()
        self.__points_per_freq = len(self.__xf) / (self.__sample_rate / 2)
        return self.__xf, np.abs(self.__yf)

    def delete_noise(self, target_idx_range=None, target_amplitude=None):
        # self.__new_yf = copy.deepcopy(self.__yf)
        if target_amplitude is None:
            meaning_target_amplitude = max(self.__yf) + 1
        else:
            meaning_target_amplitude = target_amplitude

        if target_idx_range is None and target_amplitude is None:
            target_idx = int(self.__points_per_freq * 4000)

            self.__new_yf = np.array([self.__yf[i] if (self.__yf[i] >= meaning_target_amplitude and target_idx <= i) or
                                                      (i <= target_idx) else 0 for i in range(len(self.__yf))])
        elif target_idx_range is None and target_amplitude is not None:
            self.__new_yf = np.array([self.__yf[i] if self.__yf[i] >= meaning_target_amplitude else 0 for i in range(len(self.__yf))])

        elif len(target_idx_range) == 1:
            target_idx = int(target_idx_range[0] * self.__points_per_freq)
            self.__new_yf = np.array([self.__yf[i] if (self.__yf[i] >= meaning_target_amplitude and target_idx <= i) or
                                                      (i <= target_idx) else 0 for i in range(len(self.__yf))])
        else:
            target_idx_start = int(target_idx_range[0] * self.__points_per_freq)
            target_idx_end = int(target_idx_range[1] * self.__points_per_freq)

            self.__new_yf = np.array(
                [self.__yf[i] if (self.__yf[i] >= meaning_target_amplitude and target_idx_start <= i <= target_idx_end) or
                                 (target_idx_start >= i or i >= target_idx_end) else 0
                 for i in range(len(self.__yf))])

        return self.__xf, np.abs(self.__new_yf)

    def set_new_audio(self):
        self.__yf = copy.deepcopy(self.__new_yf)
        self.__data = irfft(self.__yf)

    def get_audio(self):
        return self.__data

    def get_clear_audio(self):
        if self.__new_yf is None:
            return None
        new_sig = irfft(self.__new_yf)
        norm_new_sig = np.int16(new_sig * (32767 / new_sig.max()))
        return norm_new_sig

    def get_sample_rate(self):
        return self.__sample_rate

