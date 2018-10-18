# create new data sets for experiments

- preparation:
    1. copy cerevoice_eng/ and voice/ folders into preprocessing/
        - voice/ has to contain both voice and licence files
    2. optional: copy bbdf and refdf files to preprocessing/data/


- usage: run preprocessing/create_json.py with python 2.7 (--h for list of available arguments)
    - specify location of bbdf and refdf files with --o , if files are not in preprocessing/data
    - default output folder: preprocessing/data/output

# evaluate log files

- preparation:
    1. copy images/ , audio/ and json/ from Slurk static folder into evaluation/data/
    2. copy corresponding log file(s) into evaluation/data/

- usage: run evaluation/evaluate_logs.ipynb with Jupyter Notebook
