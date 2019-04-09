#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 12:55:36 2019

@author: zaizen
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
        self.__audio_block_list__ = sorted(glob.glob(self.__presplit_path__ + "*"))
        buildDirectoryAnyway(self.__splited_audio_path__)
        self.audioInfoDetect()

    def setMinSil(self, silence_len):
        if silence_len < 200 or silence_len > 5000:
            print(silence_len + "ms is not a proper length of a silence to split audio", file=sys.stderr)
        else:
            self.__min_silence__ = silence_len

    def audioInfoDetect(self):

        for audio_block in self.__audio_block_list__:
            self.__audio_info__.append(typeCheck(audio_block))
        print(self.__audio_info__, file=sys.stderr)

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
    # wavfile(96kHz,24bit) is not supported by basic module wave. hard to get attributes like frequency or sample width
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
    if kind.MIME == "audio/x-wav":         # Type of file is wav
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


def buildDirectoryAnyway(folder_path):
    """
    Build A New Folder.
    If The Path Exists, Overwrite ALL In The Old Directory .
    """
    try:
        os.mkdir(folder_path)

    except FileExistsError as fe:
        shutil.rmtree(folder_path)
        os.mkdir(folder_path)


if __name__ == "__main__":
    presplit_path = "../__prepAudiodata/"
    splited_audio_path = "../__audiodata/"
    a = AudioFileCutter(presplit_path, splited_audio_path)
    a.setMinSil(2000)
    a.audioSplit()

