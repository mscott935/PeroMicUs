# PeroMicUs

PeroMicUs is a simple, GUI-based bioacoustic analysis and classification program built out of a need to analyze large amounts of rodent vocal data for a behavioral assay. Unlike much existing vocal analysis software, PeroMicUs does not perform any pre-processing signal filtering to account for the particularly wide range of frequencies our test animal (*Peromyscus*) are capable of producing. As a result, this software works best when supplied controlled vocalization recordings with little to no background noise.

PeroMicUs processes audio in a systematic pipeline:

 1. Audio segmentation. Vocalizations are detected based on a set silence level measured in decibels relative to full scale (dBFS). This may be input manually by the user, or detected automatically by uploading an audio file containing only background noise from the recording chamber.
 2. Spectrogram generation. Spectrograms, representations of each vocalization in the frequency-time domain, may be automatically generated using matplotlib and saved if the user specifies.
 3. Spectral feature analysis. Using the pyAudioAnalysis library, spectral features of vocalizations deemed relevant for our particular project are collected.
 4. Classification. A pre-trained support-vector machine classifier is supplied with PeroMicUs, used for distinguishing three primary sound types: ultrasonic vocalizations, sonic vocalizations, and miscellaneous sound (both vocalizations that do not correspond to the two aforementioned types, as well as nonvocal noise like scratching). 
 5. Output writing. Per-vocalization output and per-specimen output are both saved as .csv files.

At present, PeroMicUs is expected only to function properly when processing *Peromyscus* calls using a similar recording procedure to ours. Whether or not this code will be generalized to other organisms is uncertain.

## Getting Started

PeroMicUs is built exclusively using Python. Installation of the packages in Prerequisites should be sufficient to run the program.

### Prerequisites
 - numpy
 - matplotlib
 - pandas
 - pydub
 - PyQt5
 - pyAudioAnalysis dependencies
	 - sklearn
	 - simplejson
	 - eyed3

### Installing
Download/clone the respository and run the UI file (currently prototype.py).

## Built With

* [pyAudioAnalysis](https://github.com/tyiannak/pyAudioAnalysis) - The primary audio analysis package used.

## Authors

* **Michael Scott** - *Developer*


## Acknowledgments

* Dr. Nicholas Jourjine.
* Hoekstra Lab at Harvard University.