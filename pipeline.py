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

def pipe(options):
    if not os.path.exists(options['input_dir']):
        raise exceptions.NoInputError(options['input_dir'])

    if not os.path.exists(options['output_dir']):
        os.makedirs(options['output_dir'])

    if options['bool_parseFilename']:
        fieldnames = ['source_file', 'clip_number'] \
                     + options['filename_categories'] \
                     + ['start_time', 'end_time', 'duration', 'max_dBFS', 'spectral_entropy', 'spectral_centroid', 'rolloff_90', 'rolloff_50',
                        'rolloff_25', 'rolloff_10', 'zcr', 'spectral_spread', 'type_svm', 'svm_confidence', 'notes']
    else:
        fieldnames = ['source_file', 'clip_number', 'start_time', 'end_time', 'duration', 'max_dBFS', 'spectral_entropy', 'spectral_centroid', 'rolloff_90', 'rolloff_50', 'rolloff_25', 'rolloff_10', 'zcr', 
                      'spectral_spread', 'type_svm', 'svm_confidence', 'notes']

    with open(options['output_dir'] + '/vocalizations.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

    batch_vocs = []

    with os.scandir(options['input_dir']) as files:
        for i, file in enumerate(files):
            if not file.name.endswith(".wav"):
                print(f"Non-wave file {file.name}, skipping")
                continue

            input_audio = pydub.AudioSegment.from_file(options['input_dir']+'/'+file.name, format="wav")

            if not options['bool_deleteClips']:
                if not os.path.exists(options['output_dir'] + '/clips/'):
                    os.makedirs(options['output_dir'] + '/clips/')

            vocs = segment(input_audio, file.name, options)

            if options['bool_makeSpectrograms']:
                if not os.path.exists(options['output_dir'] + '/spectrograms/'):
                    os.makedirs(options['output_dir'] + '/spectrograms/')
                plotSpectrograms(vocs, options['output_dir'])

            analyze(vocs)

            classify(vocs)

            batch_vocs = batch_vocs + vocs

            write_output(vocs, options['output_dir'], fieldnames)

            write_pup_csv(options['output_dir'], options)

    return batch_vocs

def segment(input_audio, filename, options):
    # Collect samples, start times and end times

    if options['bool_analyze_full']:
        audio = input_audio
    else:
        if utils.validTimeBounds(options['start_time'], options['end_time'], len(input_audio)):
            audio = input_audio[options['start_time']:options['end_time']]
        else:
            raise exceptions.TimeBoundError(options['start_time'], options['end_time'], filename)

    # Set silence thresholds
    if options['bool_inferSilence']:
        try:
            silence = pydub.AudioSegment.from_file(options['silenceFilename'], format="wav")
            silence_thresh = silence.max_dBFS
        except FileNotFoundError:
            print(f"Silence file not found, defaulting to spinbox value {options['silenceThreshold']}.")
            silence_thresh = options['silenceThreshold']
    else:
        silence_thresh = options['silenceThreshold']

    min_silence_len = options['silenceMinLen']
    keep_silence = options['silenceBuffer']

    clips = pydub.silence.split_on_silence(audio, min_silence_len=min_silence_len,
                                                silence_thresh=silence_thresh,
                                                keep_silence=keep_silence)
    nonsilent_ranges = pydub.silence.detect_nonsilent(audio,
                                                        min_silence_len=min_silence_len,
                                                        silence_thresh=silence_thresh)

    # Parse filename
    if options['bool_parseFilename']:
        filename_info = utils.parseFileName(filename, options['filename_delimiter'], options['filename_categories'])
    else:
        filename_info = {}

    # Init list for vocalizations, then iterate through clipped audio and make new dict for each
    clip_list, clip_index, skipped = [], 0, 0
    for clip in tqdm(clips, desc="Segmenting audio: ", ascii=True):
        if options['bool_removeClipped']:
            if max(clip.get_array_of_samples()) >= (clip.max_possible_amplitude - 1):
                skipped += 1
                clip_index += 1
                continue
        d = {
            'source_file': filename[:-4],
            'clip_number': clip_index - skipped,
            'start_time': nonsilent_ranges[clip_index][0] + options['start_time'] - keep_silence,
            'end_time': nonsilent_ranges[clip_index][1] + options['start_time'] + keep_silence,
            'duration': nonsilent_ranges[clip_index][1] - nonsilent_ranges[clip_index][0] + (2 * keep_silence),
            'max_dBFS': clip.max_dBFS,
            'audio': np.asarray(clip.get_array_of_samples().tolist()),
            'framerate': clip.frame_rate,
        }
        clip_list.append({**filename_info, **d})
        
        # Export clip
        if not options['bool_deleteClips']:
            clip.export(f"{options['output_dir']}/clips/{filename[:-4]}_voc_{clip_index - skipped}.wav", format="wav")

        clip_index += 1
    
    return clip_list

def plotSpectrograms(vocs, output_dir):
    for i, voc in enumerate(tqdm(vocs, desc="Spectrogram generation: ", ascii=True)):
        audio, rate, source = voc['audio'], voc['framerate'], voc['source_file']
        plt.specgram(audio, Fs=rate, cmap='plasma')
        plt.ylabel('Frequency (Hz)')
        plt.xlabel('Time (s)')
        plt.title(f"Vocalization {i}")

        plt.savefig(output_dir + f"/spectrograms/{source}_spec_{i}", bbox_inches="tight")

        plt.clf()

        voc['spectrogram_file'] = output_dir + f"/spectrograms/{source}_spec_{i}"

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

        res, P, _ = audioTrainTest.segmentClassification(x, 'classifiers/SMV_RBF_new', 'svm_rbf')

        if int(res) == 0: voc['type_svm'] = 'sonic'
        elif int(res) == 1: voc['type_svm'] = 'ultrasonic'
        else: voc['type_svm'] = 'scratch'

        voc['svm_confidence'] = P[int(res)]

def write_output(vocs, output_dir, fieldnames):
    with open(output_dir + '/vocalizations.csv', 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
        for voc in vocs:
            if voc['type_svm'] == 'sonic' and (voc['duration'] <= 30 or voc['duration'] >= 300):
                voc['notes'] = 'anomalous duration'
            writer.writerow(voc)

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
