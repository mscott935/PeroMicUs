import csv
import os
import sys
import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pydub
from tqdm import tqdm

import utils
import exceptions
from pyAudioAnalysis import (audioBasicIO, audioFeatureExtraction,
                             audioTrainTest)

MT_WIN, MT_STEP = 2048, 1024
ST_WIN, ST_STEP = 256, 128

def process(input_dir, features_output_dir, segments_file, animal_name):
    
#input_dir is the directory containing the audio file for a single animal
#features_output_dir is the features directory for that animal
#segments file is the absolute path to the ava - generated segments file.
#animal_name is the name of the animal directory for the animal

    wav_file_name = animal_name + '.wav'
    path_to_wav_file = input_dir+'/'+ wav_file_name
    
    #check that the input and features output directories exist
    if not os.path.exists(input_dir): raise exceptions.NoInputError(input_dir)
    if not os.path.exists(features_output_dir): raise exceptions.NoInputError(features_output_dir)

    #define the field names (JUST FOR NOW manually look at the file name and define the categories separated by underscores)
    fieldnames = ['source_file', 'clip_number', 'species', 'parents', 'litter', 'litter_pup_number', 'age_in_days', 'date', 'time',  'start_time', 'end_time', 'duration', 'max_dBFS', 'spectral_entropy', 'spectral_centroid', 'rolloff_90', 'rolloff_50', 'rolloff_25', 'rolloff_10', 'zcr', 
                      'spectral_spread', 'type_svm', 'svm_confidence']


    #initialize the list of vocal features. Each item in this list will be a dictionary whose keys are fieldnames.
    batch_vocs = []
            
    #load the audio using pydub
    input_audio = pydub.AudioSegment.from_file(input_dir+'/'+ animal_name + '.wav', format="wav")

    #segment the audio using the ava segments file
    vocs = segment(input_audio = input_audio, filename = wav_file_name, timestamp_file = segments_file)            
            
    # get some spectral features using pyaudio analysis - this is the analyze function
    for voc in tqdm(vocs, desc="Vocalization Analysis: ", ascii=True):
        data, rate = voc['audio'], voc['framerate']
        mt_feats, _, _ = audioFeatureExtraction.mtFeatureExtraction(data, rate, MT_WIN, MT_STEP, ST_WIN, ST_STEP)
        voc['spectral_entropy'] = np.mean(mt_feats[5])
        voc['spectral_centroid'] = np.mean(mt_feats[3])
        voc['rolloff_90'] = np.mean(mt_feats[7])
        voc['rolloff_50'] = np.mean(mt_feats[8])
        voc['rolloff_25'] = np.mean(mt_feats[9])
        voc['rolloff_10'] = np.mean(mt_feats[10])
        voc['zcr'] = np.mean(mt_feats[0])
        voc['spectral_spread'] = np.mean(mt_feats[4])

    #classify the vocalization using the SVM and write the output to the features file - this is the classify function
    for voc in tqdm(vocs, desc="SVM classification: ", ascii=True):
        x = voc['audio']
        res, P, _ = audioTrainTest.segmentClassification(x, 'classifiers/SMV_RBF', 'svm_rbf')
        if int(res) == 0: voc['type_svm'] = 0  #0 means 'sonic' 
        elif int(res) == 1: voc['type_svm'] = 10 #10 means'ultrasonic'
        else: voc['type_svm'] = 1000 #1000 means 'scratch'
        voc['svm_confidence'] = P[int(res)]
            
    batch_vocs = batch_vocs + vocs

    #write the feature file 
    with open(features_output_dir + '/' + animal_name + '.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')

        writer.writeheader()
        for batch_voc in batch_vocs: writer.writerow(batch_voc)
                
    return batch_vocs

def segment(input_audio, filename, timestamp_file):
    # Use Ava-supplied timestamps. timestamp_file is the absolute path to the ava generated segments file in the segments subdirectory of each animal directory
    try:
        segments = open(timestamp_file, "r+")
        timestamps = segments.readlines()[1:]
        segments.close()
    except:
        raise exceptions.MissingTimestampFileError(filename)

    animal_name = filename[:-4]
    clips, nonsilent_ranges = [], []
    start_time = 0
    buffer = 0

    for line in timestamps:
        start, stop = map(lambda x: round(float(x)*1000), line.split()) 
        clips.append(input_audio[start:stop])
        nonsilent_ranges.append([start, stop])

    filename_info = parseFileName(filename = animal_name, delimiter = '_', categories = ['species', 'parents', 'litter', 'litter_pup_number', 'age_in_days', 'date', 'time'])

    # Init list for vocalizations, then iterate through clipped audio and make new dict for each
    clip_list, clip_index, skipped = [], 0, 0
    
    for clip in tqdm(clips, desc="Segmenting audio: ", ascii=True):

        d = {
            'source_file': filename[:-4],
            'clip_number': clip_index,
            'start_time': nonsilent_ranges[clip_index][0] + start_time - buffer,
            'end_time': nonsilent_ranges[clip_index][1] + start_time + buffer,
            'duration': nonsilent_ranges[clip_index][1] - nonsilent_ranges[clip_index][0] + (2 * buffer),
            'max_dBFS': clip.max_dBFS,
            'audio': np.asarray(clip.get_array_of_samples().tolist()),
            'framerate': clip.frame_rate,
        }
        
        clip_list.append({**filename_info, **d})

        clip_index += 1
    
    return clip_list

def analyze(vocs):
    for voc in tqdm(vocs, desc="Vocalization Analysis: ", ascii=True):
        data, rate = voc['audio'], voc['framerate']
        mt_feats, _, _ = audioFeatureExtraction.mtFeatureExtraction(data, rate, MT_WIN, MT_STEP, ST_WIN, ST_STEP)
        voc['spectral_entropy'] = np.mean(mt_feats[5])
        voc['spectral_centroid'] = np.mean(mt_feats[3])
        voc['rolloff_90'] = np.mean(mt_feats[7])
        voc['rolloff_50'] = np.mean(mt_feats[8])
        voc['rolloff_25'] = np.mean(mt_feats[9])
        voc['rolloff_10'] = np.mean(mt_feats[10])
        voc['zcr'] = np.mean(mt_feats[0])
        voc['spectral_spread'] = np.mean(mt_feats[4])

def classify(vocs):
    for voc in tqdm(vocs, desc="SVM classification: ", ascii=True):
        x = voc['audio']

        res, P, _ = audioTrainTest.segmentClassification(x, 'classifiers/SMV_RBF', 'svm_rbf')

        if int(res) == 0: voc['type_svm'] = 0  #0 means 'sonic' 
        elif int(res) == 1: voc['type_svm'] = 10 #10 means'ultrasonic'
        else: voc['type_svm'] = 1000 #1000 means 'scratch'

        voc['svm_confidence'] = P[int(res)]

def parseFileName(filename, delimiter, categories):
    # Split filename into user-defined categories.
    # Error raised if category length does not match extracted filename segments.
    segs = filename.split(delimiter)
    if len(segs) != len(categories):
        raise exceptions.FilenameParseError(filename)
    else:
        filename_info = {}
        for c, s in zip(categories, segs):
            # Trim file extensions
            if '.' in s:
                s = s.split('.')[0]
            filename_info[c] = s
        return filename_info

#def write_output(vocs, output_dir, fieldnames):
#    with open(output_dir + '/vocalizations.csv', 'a', newline='') as csvfile:
#        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
#        for voc in vocs:
#            if voc['type_svm'] == 'sonic' and (voc['duration'] <= 30 or voc['duration'] >= 300):
#                voc['notes'] = 'anomalous duration'
#            writer.writerow(voc)

def write_pup_csv(output_dir, options):
    ''' Read in vocalization csv, aggregate data by pup, and write a new csv. '''
    # Read file, get unique keys and initialize output list
    df = pd.read_csv(output_dir + '/vocalizations.csv')
    source_files = df['source_file'].unique()
    output = []

    # Group by source file and vocal type, then get means
    df_counts = df.groupby(['source_file', 'type_svm']).count()['clip_number']
    df_grouped = df.groupby(['source_file', 'type_svm']).aggregate(np.mean)

    # Specify columns we care about
    cols = ['duration', 'max_dBFS', 'spectral_entropy', 'spectral_centroid', 'rolloff_90', 'rolloff_10', 'zcr', 'spectral_spread']

    # Iterate through each filename
    for filename in source_files:
        # Initialize a new dictionary for this particular pup
        if options['bool_parseFilename']:
            d = utils.parseFileName(filename, options['filename_delimiter'], options['filename_categories'])
        else:
            d = {'source_file': filename}
        # Try to get sv count, otherwise default to 0
        try:
            d['sv_count'] = df_counts.loc[filename].loc['sonic']
        except:
            d['sv_count'] = 0

        # Same as above but usv
        try:
            d['usv_count'] = df_counts.loc[filename].loc['ultrasonic']
        except:
            d['usv_count'] = 0

        # For every entry we care about try to get its mean and store in dict, otherwise set as None (blank)
        for col in cols:
            data = df_grouped.loc[filename][col]
            try:
                sv_mean = data.loc['sonic']
            except:
                sv_mean = None
            try:
                usv_mean = data.loc['ultrasonic']
            except:
                usv_mean = None

            d[f"sv_{col}"] = sv_mean
            d[f"usv_{col}"] = usv_mean
        
        output.append(d)

    # Write csv file
    with open(output_dir + '/pups.csv', 'w', newline='') as csvfile:
        fieldnames = list(d.keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        for d in output:
            writer.writerow(d)
