import csv
import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pydub

import exceptions
from pyAudioAnalysis import audioFeatureExtraction

MT_WIN, MT_STEP = 2048, 1024
ST_WIN, ST_STEP = 256, 128

def analyze_syllables(input_filename, timestamp_filename=None):
    """ 
    Perform spectral analysis on syllables in input_filename.
  
    Optional timestamp_filename may be passed in and parsed for timestamps, otherwise
    syllables will be automatically detected using pydub's silence detection. Timestamp file
    must be in ava format. Acoustic features are gathered using pyAudioAnalysis and returned
    as a pandas dataframe.
  
    Parameters: 
    input_filename (str): Filename of audio to analyze.
    timestamp_file (str) (optional): Filename of ava-generated timestamps.
  
    Returns: 
    analyzed_clip_df (pandas.DataFrame): Database-style container of acoustic features per syllable.
    """

    input_audio = pydub.AudioSegment.from_file(input_filename, format="wav")
    audio_framerate = input_audio.frame_rate

    if timestamp_filename:
        try:
            with open(timestamp_filename) as f:
                timestamp_lines = f.readlines()[1:] # skip header
            timestamps = []
            for line in timestamp_lines:
                start, stop = map(lambda x: round(float(x) * 1000), line.split()) # milliseconds -> seconds
                timestamps.append([start, stop])
        except:
            raise exceptions.MissingTimestampFileError(timestamp_filename)
    else:
        timestamps = pydub.silence.detect_nonsilent(input_audio,
                                                    min_silence_len=5,
                                                    silence_thresh=-55)
    
    # Segment audio
    clips = [input_audio[start:stop] for start, stop in timestamps]

    # Analyze clips
    analyzed_clips = []
    for i, clip in enumerate(clips):
        mt_feats, _, ft_names = audioFeatureExtraction.mtFeatureExtraction(np.asarray(clip.get_array_of_samples().tolist()),
                                                                    audio_framerate, MT_WIN, MT_STEP, ST_WIN, ST_STEP)
        clip_data = {
            'animal_name': input_filename[:-4],
            'syllable_number': i,
            'syllable_start_time': timestamps[i][0],
            'syllable_end_time': timestamps[i][1],
            'syllable_duration': timestamps[i][1] - timestamps[i][0],
            'intersyllable_duration': timestamps[i+1][0] - timestamps[i][1] if i < len(clips) - 1 else None,
            'max_dBFS': clip.max_dBFS,
        }

        # TODO: Not right! Feature names != actual features because we have weird rolloffs predefined
        feature_data = {name : value for name, value in zip(ft_names, map(np.mean, mt_feats))}
        clip_data.update(feature_data)

        analyzed_clips.append(clip_data)

    return pd.DataFrame(analyzed_clips)

def aggregate_by_animal(syllable_data):
    """ 
    Group syllable data by animal.
  
    Unique animals are determined by the filename (i.e. the 'animal_name' field of analyzed dataframe).
    Counts total vocalizations of each type and provides arithmetic mean of acoustic features per each
    vocalization type.
  
    Parameters: 
    syllable_data (pandas.DataFrame): 
  
    Returns: 
    analyzed_clip_df (pandas.DataFrame): Database-style container of acoustic features per syllable.
    """
    raise NotImplementedError

def classify_syllable(clip, model_name):
    """ 
    Classify syllable as cry (0), whistle (1) or neither (2).
  
    Parameters: 
    clip (pydub.AudioSegment): Input syllable.
    model_name (str): Name of the pyAudioAnalysis classification model to be used.
  
    Returns: 
    type (int): Database-style container of acoustic features per syllable.
    confidence (float): Probability estimate.
    """
    raise NotImplementedError
