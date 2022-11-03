# Vinylset
## Step 1: Download the data
`
wget -i url_list.txt
`
## Step 2: Install virtualenv (Python 3.9)
```
  pip install virtualenv
  virtualenv vinylset source vinylset/venv/bin/activate
  pip -r requirements.txt
```

## Step 3: 
To preprocess the data run:
```
python3 input/path/downloaded/tracks output/path/preprocessed/tracks
```
This will process files as done in the VInlyset corpus.
MOS labels are in `vinylset_MOS.txt`
