#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 15:33:50 2019
Goal: Convert wavfile into standard form (raw file) as openjtalk-model-training data.
Attention: Current version only support wavfiles with 96kHz 32bit(interger) mono channel
Abstract of audio processing (take 32bit integer 96kHz wavfile as an example)
1. convert 32bit integer to32bit float
2. down sample-rate(frequency) 96kHz to 48kHz
3. down sample-width(bit) 32bit to 16bit
4.obtain raw file
@author: peng_zaizen
"""

import os
import glob
# pydub is fine but it always convert 24bit wavfile to 32bit wavfile ! Sometime this feature could be useful
import wave
import shutil
import sys


class AudioPreProcesser:
    def __init__(self, db_name="normal_daily", wav_audio_path="../data/", raw_audio_path="../raw/"):
        self.__db_name = db_name
        self.__wav_audio_path = inputAsPath(wav_audio_path)
        self.__raw_audio_path = inputAsPath(raw_audio_path)
        self.__wav_audio_record = []
        buildDirectoryAnyway(self.__raw_audio_path)
        wavfile_path_list = sorted(glob.glob(self.__wav_audio_path + "*.wav"))

        for wavfile_record in wavfile_path_list:  # get filename and the filename extension and store them as a set
            temp_channel, temp_frame_rate, temp_sample_width = extractAudioFeature(wavfile_record)
            filename_set = wavfile_record.split("/")[-1].split(".")
            filename_set.append(temp_channel)
            filename_set.append(temp_frame_rate)
            filename_set.append(temp_sample_width)
            self.__wav_audio_record.append(filename_set)

    def printFileList(self):
        for i in self.__wav_audio_record:
            print(i, file=sys.stderr)

    def wavfileProcessing(self):

        # print(self.__wav_audio_record, file=sys.stderr)
        unsupport_counter = 0
        audio_path_temp = "../temp/"
        buildDirectoryAnyway(audio_path_temp)
        counter = 1
        for file in self.__wav_audio_record:
            if audioFormatCheck(wavfile=(self.__wav_audio_path + file[0] + "." + file[1])) is False:
                os.system("echo " + "File " + file[0] + "." + file[1] + " is not supported")
                unsupport_counter = unsupport_counter + 1
                continue

            if file[4] == 16:
                if file[3] == 48000:
                    wavToRaw(self.__wav_audio_path + file[0] + "." + file[1],
                             self.__raw_audio_path + self.__db_name + str("{0:04d}".format(counter)) + ".raw")
                else:
                    unsupport_counter = unsupport_counter + 1
                    continue
            elif file[4] == 32:
                wavIntToFloat(self.__wav_audio_path + file[0] + "." + file[1], audio_path_temp + file[0] + "f.wav")
                if file[3] == 96000:
                    wavToRaw(audio_path_temp + file[0] + "f.wav", audio_path_temp + file[0] + "r.raw")
                    # print(raw_folder + file[0] + "." + file[1], raw_folder + file[0] + "r.raw", file=sys.stderr)

                    downFrequency(audio_path_temp + file[0] + "r.raw", audio_path_temp + file[0] + "rds.raw")
                    # print(raw_folder + file[0] + "r.raw", raw_folder + file[0] + "rds.raw", file=sys.stderr)
                    rawToWav(audio_path_temp + file[0] + "rds.raw", audio_path_temp + file[0] + "rdsw.wav")
                    # print(raw_folder + file[0] + "rds.raw", raw_folder + file[0] + "rdsw.wav", file=sys.stderr)
                    downSampleWidth(audio_path_temp + file[0] + "rdsw.wav", audio_path_temp + file[0] + "rdswb.wav")
                    wavToRaw(audio_path_temp + file[0] + "rdswb.wav",
                             self.__raw_audio_path + self.__db_name + str("{0:04d}".format(counter)) + ".raw")
                elif file[3] == 48000:
                    downSampleWidth(audio_path_temp + file[0] + "f.wav", audio_path_temp + file[0] + "rdswb.wav")
                    wavToRaw(audio_path_temp + file[0] + "rdswb.wav",
                             self.__raw_audio_path + self.__db_name + str("{0:04d}".format(counter)) + ".raw")
                else:
                    unsupport_counter = unsupport_counter + 1
                    continue
            else:
                unsupport_counter = unsupport_counter + 1
                continue

            counter = counter + 1

        if unsupport_counter > 0:
            print("Ignored some unsupported audio", file=sys.stderr)

        else:
            print("All wavfile processed", file=sys.stderr)



def buildDirectory(folder_path="../rawfolder/"):
    """
    Build A New Folder.
    If The Path Exists, The Build Fail .
    """
    try:
        os.mkdir(folder_path)
        return True
    except FileExistsError as fe:
        # print(folder_path+" Already Existed.", file=sys.stderr)
        return False


def buildDirectoryAnyway(folder_path):
    """
    Build A New Folder.
    If The Path Exists, Overwrite ALL In The Old Directory .
    """
    try:
        os.mkdir(folder_path)
        return True
    except FileExistsError as fe:
        shutil.rmtree(folder_path)
        os.mkdir(folder_path)
        # print("Though "+folder_path+" Already Existed. Overwrite it anyway", file=sys.stderr)
        return True


def extractAudioFeature(wavfile):
    audio_file = wave.open(wavfile, 'r')
    channel = audio_file.getnchannels()
    frame_rate = audio_file.getframerate()
    sample_width = audio_file.getsampwidth() * 8
    return channel, frame_rate, sample_width


def audioFormatCheck(wavfile):
    """
    Check The Wavfile As Input Data
    True : standard form
    false : non-standard form
    """
    channel, frame_rate, sample_width = extractAudioFeature(wavfile)

    if channel != 1:
        return False
    else:
        if frame_rate == 48000 and sample_width == 32:
            return True
        elif frame_rate == 48000 and sample_width == 16:
            return True
        elif frame_rate == 96000 and sample_width == 32:
            return True
        else:
            return False


def wavIntToFloat(int_wavfile, float_wavfile):
    """
    for 32bit wavfile, convert integer form to float form
    """
    cmd = "sox " + int_wavfile + " -e floating-point " + float_wavfile
    os.system(cmd)


def wavToRaw(wavfile, rawfile):
    """
    wipe the header
    """
    cmd = "sox " + wavfile + " " + rawfile
    if os.path.exists(wavfile):
        os.system(cmd)
        os.remove(wavfile)


def downFrequency(high_frequency_file, low_frequency_file):
    """
    downsampling from 96000 to 48000 so it's 2:1 ->21

    """
    cmd = " ds -s 21 " + high_frequency_file + " > " + low_frequency_file
    if os.path.exists(high_frequency_file):
        os.system(cmd)
        os.remove(high_frequency_file)


def rawToWav(rawfile, wavfile):
    """
    form raw to wav(frequency_rate=48000.bit=32 float)
    """
    cmd = "sox -r 48000 -b 32 -e float " + rawfile + " " + wavfile
    if os.path.exists(rawfile):
        os.system(cmd)
        os.remove(rawfile)


def downSampleWidth(high_sample_width_file, low_sample_width_file):
    """
    from 32bit(float)wave file to 16bit integer wavefile
    only for 32bit float form to 16bit integer form
    """

    cmd = "sox " + high_sample_width_file + " -b 16 " + low_sample_width_file
    if os.path.exists(high_sample_width_file):
        os.system(cmd)

        os.remove(high_sample_width_file)


def inputAsPath(path_str):
    path = list(path_str)
    if path[-1] is not '/':
        path.extend('/')
    path_str = ''.join(path)
    return path_str

# ==============================================================================
#
# def main():
#     a = AudioPreProcesser(wav_audio_path="../__audiodata/", raw_audio_path="../rawA")
#     #a.wavToRaw()
#     a.printFileList()
#
#
# if __name__ == "__main__":
#     main()
# ==============================================================================