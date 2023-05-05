import os
import subprocess
import soundfile as sf
import math
import librosa
import click
import re
import numpy as np

@click.command()
@click.argument('in_path', type=click.Path(exists=True))
@click.argument('out_path', type=click.Path(exists=True))
def preproc(in_path, out_path):
    """Preprocessing audio for vinylset.

    in_path - is the absolute path where the audio tracks are stored.
    
    out_path - is the absolute path where saving preprocessed tracks.
    """

    target_freq = 44100
    for id_file, file in enumerate(os.listdir(in_path)):
        print(f'ID: {id_file}  -  FILE: {file}')
        filename, _ = os.path.splitext(file)
        target_filename = re.sub('\W+', '', filename)
        if not os.path.isdir(out_path):
            os.mkdir(out_path)
        filepath = os.path.join(in_path, file)

        # Out filepath
        use_subdir = False
        if use_subdir:
            out_subdir = os.path.join(out_path, filepath.split('/')[-2])
            if not os.path.isdir(out_subdir):
                os.mkdir(out_subdir)
            out_path = os.path.join(out_path, out_subdir)
            out_filepath = os.path.join(out_path, out_subdir, target_filename + '.wav')
        else:
            target_filename, _ = os.path.splitext(target_filename)
            out_filepath = os.path.join(out_path, target_filename + '.flac')

        where = 'middle'
        # Take before or middle or after and write to file (middle is the default behaviour)
        wave, _ = librosa.load(filepath, sr=target_freq, mono=False)
        if (len(wave.shape) == 1):
            wave = np.expand_dims(wave, 1).T
        
        if wave.shape[1] >= 10*target_freq:
            if where == 'middle':
                start = wave.shape[1]//2 - math.floor(5 * target_freq)
                end = wave.shape[1]//2 + math.ceil(5 * target_freq)
            elif where == 'before':
                start = wave.shape[1]//2 - math.floor(15 * target_freq)
                end = wave.shape[1]//2 - math.ceil(5 * target_freq)
                out_filepath = os.path.splitext(out_filepath)[0] + '_' + where + '.wav'
            elif where == 'after':
                start = wave.shape[1]//2 + math.floor(5 * target_freq)
                end = wave.shape[1]//2 + math.ceil(15 * target_freq)    
                out_filepath = os.path.splitext(out_filepath)[0] + '_' + where + '.wav' 
            wave = wave[:,start:end]

        sf.write(out_filepath, wave.T, samplerate=target_freq, format='flac')

        # Convert to AAC HE 320
        if use_subdir:
            dst_filepath = os.path.join(out_path, target_filename.split('.')[0] + '_aache320.m4a')
        else:
            dst_filepath = os.path.join(out_path, target_filename + '_aache320.m4a')
        aache_320 = f'ffmpeg -i {out_filepath} -ac 2 -ar {target_freq} -c:a libfdk_aac -b:a 320k -profile:a aac_he {dst_filepath}'.split(' ')
        subprocess.call(aache_320)
        os.remove(out_filepath)

        # Convert to wav (it will not improve audio quality, it's just better when integrating with some load functions that might expect wav files)
        dst_filepath_wav = os.path.splitext(dst_filepath)[0] + '.wav'
        #if not os.path.isfile(dst_filepath_wav):
        wav_convert = f'ffmpeg -i {dst_filepath} {dst_filepath_wav}'.split(' ')
        subprocess.call(wav_convert)
        os.remove(dst_filepath)
        
        # Loudness normalization EBU 128
        dst_filepath_norm = os.path.splitext(dst_filepath)[0] + '_ln.wav'
        loudnorm = f'ffmpeg -y -i {dst_filepath_wav} -filter:a loudnorm -ar {target_freq} -y {dst_filepath_norm}'.split(' ')
        subprocess.call(loudnorm)
        os.remove(dst_filepath_wav)
        print(f'OUTPUT FILE: {dst_filepath_norm}')

if __name__ == '__main__':
    preproc()