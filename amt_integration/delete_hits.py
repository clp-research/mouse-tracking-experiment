import os
import aws_config
import json
from datetime import datetime

files = ["published/"+f for f in os.listdir('published') if f.endswith('.json')]

print ("files found: ", files)

hits = []

for file in files:
    json_data=open(file).read()
    data = json.loads(json_data)
    for i in data:
        hits.append(i['hit_id'])

for hit in hits:
    try:
        print ('deleting hit {id}'.format(id=hit))
        aws_config.ConnectToMTurk.mturk.update_expiration_for_hit(HITId=hit,ExpireAt=0)
        aws_config.ConnectToMTurk.mturk.delete_hit(HITId=hit)
    except:
        pass

for file in files:
    print ("deleting file {file}".format(file=file))
    os.remove(file)
