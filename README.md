# Vinylset
## Purpose
Vinylset includes 620 tracks extracted from original vinyl recordings and labelled them with mean opinion score (MOS). The dataset includes original real-world recordings and represent a very challenging scenario to develop quality models. The preservation of cultural heritage through audio archives is primarily focused on the process of digitization, which involves curating audio collections from various analog media formats like wax cylinders, vinyl discs, and 78 RPMs. The purpose of Vinylset is allowing researchers to develop quality models for music collections in order to improve accessibility and usability.

Unlike traditional speech quality datasets, each recording is a quality condition. MOS human ratings are obtained from 506 participants, with an average of 15 scores per track.
Detailed information on Vinylset can be found in the ICASSP paper. 

This dataset has been used to create the [QAMA model](https://github.com/alessandroragano/music-archive-quality-prediction) which is a reference-free metric for vinyl collections. 

## Download
Recordings are sourced from the Internet Archive. After cloning the repo follow the instructions below to download the dataset. 

```
mkdir data
cd data
wget -i url_list.txt
```

This will download the tracks to the directory `data`

## Preprocessing
Vinylset tracks have been preprocessed to collect MOS human ratings and to develop the QAMA model. Preprocessing consists of 
* 10 seconds segment extracted in the middle of each track
* Conversion to HE-AAC 320 kbps to avoid network stalling

To apply the same preprocessing install [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/) and follow the instructions below.

### Step 1: Install the virtual environment
```
  mkvirtualenv -p python3.9 vinylset
  workon vinylset
  pip install -r requirements.txt
```

### Step 2: Compile ffmpeg for libfdk-aac (Linux)
The HE-AAC codec is required to convert the audio tracks. To use this codec you need to compile `ffmpeg` since it is not provided in the `apt` package.
To compile ffmpeg follow these [instructions](https://trac.ffmpeg.org/wiki/CompilationGuide/Ubuntu).

### Step 3: Run Preprocessing 
Run the python script to apply preprocessing:
```
mkdir preproc_data
python vinylset_preprocessing.py data preproc_data
```
This will process files as done in the Vinlyset corpus.
MOS labels are in `vinylset_MOS.txt`

## Paper and license
If you use Vinylset please cite this paper: 

A. Ragano, E. Benetos, and A. Hines "Audio Quality Assessment of Vinyl Music Collections using Self-Supervised Learning", in IEEE International Conference on Acoustics, Speech, and Signal Processing (ICASSP) 2023 (link will be up soon).


The dataset is licensed under the Internet Archive [copyright policy](https://help.archive.org/help/rights/).

The code is licensed under MIT license.

## Missing Tracks
Vinylset tracks are downloaded from the Internet Archive so they could be removed at anytime. If tracks are missing you can contact me: alessandroragano@gmail.com
