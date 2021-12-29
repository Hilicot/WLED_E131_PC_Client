import pyaudio  # installed pyaudio fork with wheel (https://github.com/intxcc/pyaudio_portaudio/releases)
from scipy.fft import fft
import numpy as np
import platform
from typing import Union, Any


DEBUG = False

CHUNK = 1024
FORMAT = pyaudio.paInt16
PLOT_MAX_FREQUENCY_SHOWN = 1500


def start_audio_stream(p, audio_device: str) -> tuple:
    # FIXME audio not working on Linux -> fix or use other framework instead of pyaudio
    useloopback = False

    # Get device info
    audio_device_name = audio_device.split(",")[0]
    api_name = audio_device.split(",")[1]
    device_info = p.get_device_info_by_index(0)  # throws exception if there is no device available
    for i in range(0, p.get_device_count()):
        device_info = p.get_device_info_by_index(i)
        if device_info['name'] == audio_device_name and p.get_host_api_info_by_index(device_info["hostApi"])[
            "name"] == api_name:
            break

    channelcount = max(device_info["maxOutputChannels"], device_info["maxInputChannels"])
    rate = int(device_info["defaultSampleRate"])

    if platform.system() == "Wndows":
        # Choose between loopback or standard mode
        is_input = device_info["maxInputChannels"] > 0
        if not is_input:
            useloopback = True;

        stream = p.open(format=FORMAT,
                        channels=channelcount,
                        rate=rate,
                        input=True,
                        frames_per_buffer=CHUNK,
                        input_device_index=device_info["index"],
                        as_loopback=useloopback)
    else:
        stream = p.open(format=FORMAT,
                        channels=channelcount,
                        rate=rate,
                        input=True,
                        frames_per_buffer=CHUNK,
                        input_device_index=device_info["index"])

    return stream, rate


def get_audio_level(stream, bits:int = 4096):
    data = np.frombuffer(stream.read(bits), np.int16)
    return np.max(data)


def get_normalized_audio_level(stream, max_level, min_level, max_sensitivity=1500, max_threshold=0.6, max_decay=0.01,min_sensitivity=1000, min_threshold=0.6, min_decay=0.1) -> Union[Any,int]:
    """
    return normalized audio_level

    :param max_sensitivity: max_level can never drop down this value
    :param max_threshold: when audio level goes under threshold*max_level, start dropping the max_level
    :param max_decay: how fast the max_level decreases over time
    :param min_decay:
    :param min_threshold:
    :param min_sensitivity:
    :param min_level:
    :param max_level: a parameter for the maximum audio level, which would be displayed with max brightness. to reach best effect, it must be the same parameters for all successive calls of this function
    :param stream:
    :return: float in range [0,1]
    """
    audio_level = get_audio_level(stream, 2048)

    # decrease a bit the max audio level only if audio_level is under the threshold
    if audio_level > max_level:
        max_level = audio_level
    elif audio_level < max_level*max_threshold:
        max_level -= max_decay*(max_level - audio_level)
    max_level = max(max_level,max_sensitivity)

    # do the same for min_level
    if audio_level < min_level:
        min_level = audio_level
    elif audio_level*min_threshold > min_level:
        min_level += min_decay*(audio_level - min_level)
    min_level = min(min_level,min_sensitivity)

    return (audio_level-min_level)/(max_level-min_level), max_level, min_level


def get_audio_spectrum(stream, rate):
    num_bins = int(min(CHUNK//2, np.floor(PLOT_MAX_FREQUENCY_SHOWN*CHUNK/rate)))
    data = np.frombuffer(stream.read(CHUNK), np.int16)
    fft_data = fft(data)
    norm_data = fft_data/CHUNK
    magnitudes = np.abs(norm_data[range(num_bins)])
    return magnitudes


def list_available_audio_devices() -> tuple:
    p = pyaudio.PyAudio()
    devices = []
    default_device = ""
    default_device_id = 0
    for i in range(0, p.get_device_count()):
        info = p.get_device_info_by_index(i)
        device_label = info["name"] + "," + p.get_host_api_info_by_index(info["hostApi"])["name"]
        devices.append(device_label)

        """default device = first available device in list:
                - Speakers (Realtek(R) Audio)
                - first available WASAPI device
                - first available device (any)
                - ""
                """
        # TODO On windows select only WASAPI devices, on Linux show all
        #if (p.get_host_api_info_by_index(info["hostApi"])["name"]).find("WASAPI") != -1:
        if info['name'].find("Speakers (Realtek(R) Audio)") != -1:
            default_device = device_label
            default_device_id = i
        if default_device == "":
            default_device = device_label
            default_device_id = i

    p.terminate()

    return devices, default_device, default_device_id
