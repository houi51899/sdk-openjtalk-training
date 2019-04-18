#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 12:55:36 2019

In splitting, module "Pydub" converts wavfile by default(test in 48kHz sample rate).
16bit signed integer -----> 16bit signed integer
24bit signed integer -----> 32bit signed integer
32bit signed integer -----> 32bit signed integer
32bit float          -----> 32bit signed integer


"""
from pydub import AudioSegment
import filetype
from pydub.silence import split_on_silence
import os
import glob
import shutil
import sys


class AudioFileCutter:
    def __init__(self, presplit_path, splited_audio_path):
        self.__presplit_path__ = presplit_path
        self.__splited_audio_path__ = splited_audio_path
        self.__audio_info__ = []
        self.__min_silence__ = None
        self.__audio_block_list__ = sorted(glob.glob(self.__presplit_path__ + "*.wav"))
        buildDirectoryAnyway(self.__splited_audio_path__)
        self.audioInfoDetect()

    def setMinSil(self, silence_len):
        if silence_len < 200 or silence_len > 5000:
            print(silence_len + "ms is not a proper length of the silence to split audio", file=sys.stderr)
        else:
            self.__min_silence__ = silence_len

    def audioInfoDetect(self):
        for audio_block in self.__audio_block_list__:
            self.__audio_info__.append(typeCheck(audio_block))

    def audioSplit(self):     # format of __audio_info__ : [valid_flag,file_path,file_type]
        file_order = 1
        if self.__min_silence__ is None:
            print("please set silence length used to split audio! ", file=sys.stderr)
        else:
            for record in self.__audio_info__:
                if record[0] is False:
                    continue
                else:
                    file_order = splitAndOrder(record[1], self.__splited_audio_path__, self.__min_silence__, file_order)


def typeCheck(file_path):
    # wavfile(96kHz,24bit) is not supported by module "wave". it's hard to get attributes like sample rate or bit-depth
    # so module "filetype" used instead.
    type_info = []
    valid_flag = False
    path_info = file_path
    file_type = None
    kind = filetype.guess(file_path)
    if kind is None:
        type_info.append(valid_flag)
        type_info.append(path_info)
        type_info.append(file_type)
        return type_info
    if kind.MIME == "audio/x-wav":         # .wav
        file_type = "wav"
        valid_flag = True
        type_info.append(valid_flag)
        type_info.append(path_info)
        type_info.append(file_type)
        return type_info
    else:
        file_type = kind.MIME
        type_info.append(valid_flag)
        type_info.append(path_info)
        type_info.append(file_type)
        return type_info


def splitAndOrder(audio_block, splited_audio_path, min_silence, audio_order):
    """
    :param audio_block: the wavfile to be split
    :param splited_audio_path: directory stores post-split wavfile.
    :param min_silence:
    :param audio_order: order to appear on the filename
    :return: return the order of next file
    """
    name = audio_block.split("/")[-1].split(".")[0]
    print(name, file=sys.stderr)
    sound = AudioSegment.from_file(audio_block, format="wav")
    chunks = split_on_silence(sound, min_silence_len=min_silence, silence_thresh=-60, keep_silence=600)
    for k, chunk in enumerate(chunks):
        chunk.export(
            splited_audio_path + name + "_" + str("{0:04d}".format(audio_order)) + ".wav",
            format="wav")
        audio_order = audio_order + 1
    return audio_order


def buildDirectoryAnyway(directory_path):
    """
    New a target directory.
    If the directory exists, delete it and make a new one .
    """
    try:
        os.mkdir(directory_path)
    except FileExistsError as fe:
        shutil.rmtree(directory_path)
        os.mkdir(directory_path)


if __name__ == "__main__":
    presplit_path = "../__preaudio/"
    splited_audio_path = "../__audiodata/"

    a = AudioFileCutter(presplit_path, splited_audio_path)
    a.setMinSil(1300)
    a.audioSplit()

