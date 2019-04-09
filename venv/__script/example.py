#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 12:55:36 2019

@author: zaizen
"""
import getopt
import os
import sys

import audioPreProcessing as app
import textPreProcessing as tpp


def main(argv):
    db_name = "nobu_daily"
    origin_text_file = "../__text.txt"
    label_path = "../label/"
    wav_audio_path = "../__audiodata/"
    raw_audio_path = "../raw/"

    try:
        options, args = getopt.getopt(argv, "n:t:w:r:l:h", ["name=", "text=", "wav=", "raw=", "label=", "help"])
    except getopt.GetoptError:
        print("Parameter Error! \n Program closed.", file=sys.stderr)
        sys.exit(1)

    for option, value in options:
        if option in ("-h", "--help"):
            print("This is a program to handle the processing of text and audio data \n"
                  "for training acoustic model in openjtalk.\n"
                  "====================================================================\n"
                  "Usage \n"
                  "Following command is recommanded \n"
                  "'python3 example.py -n nobu -t ../__text.txt -r ../raw/ -w ../__audiodata/ -l ../label/' \n"
                  "or simply 'python3 example.py' \n"
                  "Good luck! \n"
                  , file=sys.stderr)
            sys.exit(0)
        if option in ("-n", "--name"):
            db_name = value
        if option in ("-t", "--text"):
            if os.path.exists(value) is True:
                origin_text_file = value
            else:
                print("Text file is not found in the input directory!", file=sys.stderr)
                sys.exit(1)
        if option in ("-w", "--wav"):
            wav_audio_path = inputAsPath(value)
        if option in ("-r", "--raw"):
            raw_audio_path = inputAsPath(value)
        if option in ("-l", "--label"):
            label_path = inputAsPath(value)

    print("Current setting \n" +
          "Name: "+db_name+"\n" +
          "Text file path: "+os.path.abspath(origin_text_file)+"\n" +
          "Audio data(wav) path: "+os.path.abspath(wav_audio_path)+"\n" +
          "Audio data(raw) path: "+os.path.abspath(raw_audio_path)+"\n" +
          "Label file path: "+os.path.abspath(label_path)+"\n"
          , file=sys.stderr)

    """
    For text preprocessing:
        1.set a name for the output files. The output files will be named as [Input Name][number(0~)].lab
        2.Change the directory of (one) text file from which you want to extract labels.
        3.Change the directory as output directory for extract labels.
    """
    text = tpp.textPreProcessor(db_name, origin_text_file, label_path)
    text.labelProduce()

    """
    For audio preprocessing:
        1.set a name for the output files. The output files will be named as [Input Name][number(0~)].raw
        2.Change the directory to the position where you store your wavefiles.
        3.Change the directory as output directory for rawfiles.
    """
    audio = app.AudioPreProcesser(db_name, wav_audio_path, raw_audio_path)
    audio.wavfileProcessing()


def inputAsPath(path_str):
    path = list(path_str)
    if path[-1] is not '/':
        path.extend('/')
    path_str = ''.join(path)
    return path_str


if __name__ == "__main__":
    main(sys.argv[1:])


