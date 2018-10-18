import pandas as pd
import numpy as np
import json
import os
import datetime
import argparse
from voice_synth import synth
from shutil import copyfile

parser = argparse.ArgumentParser()
parser.add_argument("--n", help='number of json files', default=5, type=int)
parser.add_argument("--s", help='number of entries in each json file', default=10, type=int)
parser.add_argument("--o", help='path for output', default=os.getcwd()+"/data/output/" )
parser.add_argument("--p", help='path for json input', default=os.getcwd()+"/data/" )
parser.add_argument("--i", help='path to image corpus', default="/media/dsgserve1/Corpora/External/ImageCorpora/MSCOCO/train2014")
args = parser.parse_args()

n = args.n
sample_size = args.s
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

    for m in range(n):

        # get 10 random image_ids
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
            img_destination = cwd+"/images/" + image_filename
            copyfile(img_source, img_destination)

            # create audio file with refexp and store in audio output folder
            refexp = rslt["refexp"].values[0]
            rexid = rslt["rex_id"].values[0]
            audio_filename ="{img_id}-{rex_id}.wav".format(img_id=i,rex_id=rexid)
            synth("Please click on the "+str(refexp), filename=audio_filename, outdir="audio")

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
