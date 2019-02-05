import pandas as pd
import numpy as np
import json
import os
import datetime
import argparse
import configparser
from ssml_preprocess import ssml_utterance
from voice_synth import synth
from shutil import copyfile
from PIL import Image

config = configparser.ConfigParser()
config.read('config.ini')

if 'output' in config['PATHS']:
    outdir = config['PATHS']['output']
else:
    outdir = os.getcwd()+"/data/output/"

if 'json' in config['PATHS']:
    json_path = config['PATHS']['json']
else:
    json_path = os.getcwd()+"/data/"

parser = argparse.ArgumentParser()
parser.add_argument("--s", help='number of sets to be created', default=int(config['SETTINGS']['sets']), type=int)
parser.add_argument("--n", help='number of images per set', default=int(config['SETTINGS']['images']), type=int)
parser.add_argument("--o", help='path for output', default=outdir)
parser.add_argument("--p", help='path for json input', default=json_path)
parser.add_argument("--i", help='path to image corpus', default=config['PATHS']['corpus'])
args = parser.parse_args()

n = args.s
sample_size = args.n
in_dir = os.path.abspath(args.p)
cwd = os.path.abspath(args.o)
image_dir = os.path.abspath(args.i)
timestamp = datetime.datetime.now().isoformat()

def img_filename(image_id):
    """ create img filename from id """
    id = str(image_id)
    n = 12-len(id)
    img = (n*"0")+id
    return ("COCO_train2014_"+img+".jpg")

if __name__ == '__main__':

    # make sure output directory exists
    if not os.path.exists(cwd):
        os.makedirs(cwd)
        print ("created directory: "+cwd)

    # switch to output directory
    os.chdir(cwd)

    # make sure appropriate directories exist
    folders = ["/images", "/audio", "/json"]
    for folder in folders:
        if not os.path.exists(cwd+folder):
            os.makedirs(cwd+folder)
            print("created directory: "+cwd+folder)

    # import json files as data frames
    bbdf = pd.read_json(in_dir+"/"+'mscoco_bbdf.json.gz',compression='gzip', orient='split')
    refdf = pd.read_json(in_dir+"/"+'refcoco_refdf.json.gz',compression='gzip', orient='split')
    # extract unique image_ids from refdf
    image_ids = refdf['image_id'].unique()

    print ("\ncreating data sets\n")

    for m in range(n):

        # get random image_ids
        sample = np.random.choice(image_ids, sample_size)

        #create new DataFrame with columns from refdf and bbdf
        clmns = set(list(bbdf.columns)+list(refdf.columns)+["image_filename", "audio_filename"])
        resultdf = pd.DataFrame(columns=clmns)

        #iterate through image_ids in sample,
        for i in sample:
            # pick random refexp and find respective entries in bbdf, then merge
            rfdf_img = refdf[refdf["image_id"]==i].sample(1)
            rslt = pd.merge(rfdf_img, bbdf)

            # copy the corresponding image into image output folder
            image_filename = img_filename(i)
            img_source = image_dir + "/" + image_filename
            img_destination_jpg = cwd+"/images/" + image_filename
            copyfile(img_source, img_destination_jpg)
            print ("image "+image_filename)

            # add transparent area for buttons and convert to png:

                # load image from export folder
            im_in = Image.open(img_destination_jpg)
                # set filename and destination for export file
            image_filename = os.path.splitext(image_filename)[0]+".png"
            img_destination_png = os.path.splitext(img_destination_jpg)[0]+".png"
            jpg_width, jpg_height = im_in.size
                # create transparent image (200px higher than original image)
            im_out = Image.new('RGBA', (jpg_width, (jpg_height+200)), (255,0,0,0))
                # paste original image into newly created image
            im_out.paste(im_in, (0,0))
                # save resulting image to destination path
            im_out.save(img_destination_png, "PNG", compress_level=9, optimize=True)
                # remove original image in export folder
            os.remove(img_destination_jpg)

            # Audio file creation:
            refexp = rslt["refexp"].values[0]
            tagged = rslt["tagged"].values[0]
            rexid = rslt["rex_id"].values[0]
            audio_filename ="{img_id}-{rex_id}.wav".format(img_id=i,rex_id=rexid)

            # ssml_preprocess
            utterance = ssml_utterance(refexp, tagged, prosody_rate = "slow")

            synth(utterance, filename=audio_filename, outdir="audio", textout=True)

            # add image and audio file names and append to results
            rslt["image_filename"]= image_filename
            rslt["audio_filename"]= audio_filename
            resultdf = resultdf.append(rslt, ignore_index=True)

        #return results as json file and store in json output folder
        jsondata = json.loads(resultdf.to_json(orient='index'))
        jsondata["used"]=False
        filename = 'json/{time}-{number}.json'.format(time=timestamp, number=m)
        with open(filename, 'w') as outfile:
            json.dump(jsondata, outfile, sort_keys=True, indent=1)

        print ("set complete: " + filename + "\n")

    # delete preexisting feedback audio files
    for file in ["audio/correct.wav","audio/correct.json", "audio/tryagain.wav", "audio/tryagain.json"]:
        if os.path.isfile(file):
            os.remove(file)

    # create feedback audio files
    synth("Correct.", filename="correct.wav", outdir="audio", textout=True)
    synth("Try again.", filename="tryagain.wav", outdir="audio", textout=True)
