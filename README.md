# data-preprocessing-for-openjtalk
Handle a data preprocessing.
Make data ready for acoustic model training.  

## Getting Started
Two main parts

### audio splite:audio_splite.py
  spite a big wavfile into pieces by silence in audio

### audio/textPreProcessing:sample.py
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
python3 sample.py -n nobu -t ../__text.txt -r ../raw/ -w ../__audiodata/ -l ../label/
```
Or simply 

```
python3 sample.py
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

