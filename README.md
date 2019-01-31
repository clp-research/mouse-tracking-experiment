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

# AMT integration

- preparation
  1. create config.ini (copy from config.template.ini)
  2. fill in AWS credentials, change urls if slurk is not hosted locally ('link_generator' and 'login' sections)
  3. set 'value' to 'true' if used in production ('false' for sandbox)


- publishing HITs
  - execute publish_hits.py to publish HITs on AMT (specify number of HITs using the -n argument)
  - all HIT IDs are registered in JSON files in the 'published' directory


- deleting HITs
  - execute delete_hits.py to delete all HITs found in the 'published' directory
