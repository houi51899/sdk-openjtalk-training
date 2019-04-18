# data-preprocessing-for-openjtalk
Handle a data preprocessing.
Make data ready for acoustic model training.  

supported format of input audio wave 
###block wavfile supported(split script supports more): 
(48kHz)16bit signed integer, 24bit signed integer, 32bit signed integer, 32bit float
(96kHz)24bit signed integer, 32bit signed integer, 32bit float
###splited audio supported(raw generating script supports less):
(48kHz) 16bit signed integer, 32bit signed integer
(96kHz) 32bit signed integer

tips: Here you can split your splited wavfile once more (but in a long silence parameter) 
      to convert it to a supported format

## Getting Started
Two main parts

### audio splitting:audio_split.py
  split a block wavfile into pieces by silence in audio
  When set a long duration of silence to split audio file, this script could used to convert a unsupported wavfile 
  to a supported one, which means you can split some split-already wavfiles again to convert its format. 

### audio/text data preprocessing:example.py
  convert wavfile to proper rawfile and extract labels from sentenses in script
  
  Attention : Make sure rawfile and labels are in pair with same name.  
  (though they might in different directory) 
  eg. a1.raw in ../raw/ | a1.lab(mono) in ../labels/mono/ | a1.lab(full) in ../labels/full/

### Prerequisites

OpenJtalk 1.10+
HTS engine
HTK
SPTK
HDecode
htsvoice file
SOX 
audio file(.wav 96KHz 24bit mono )
text file(.txt)
pydub

```
pip install pydub
```

### Installing

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Following command is recommanded 
```
python3 example.py -n nobu -t ../__text.txt -r ../raw/ -w ../__audiodata/ -l ../label/
```
Or simply 

```
python3 example.py
```


## Environment 

linux
python3


## Built With

* [pydub](http://pydub.com) - 

## Contributing


## Versioning

## Authors

* **Wei Peng** - ** - []()


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc

