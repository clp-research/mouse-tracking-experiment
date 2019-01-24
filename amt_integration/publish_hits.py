'''publish batches of HITs on MTurk'''
import time
import json
import argparse
import sched

import aws_config
from slurk_link_generator import insert_names_and_tokens

RESULTS = []
# image files to be shown in AMT
SLIDES = ['https://raw.githubusercontent.com/nilinykh/meetup_instructions/master/0001.jpeg',
          'https://raw.githubusercontent.com/nilinykh/meetup_instructions/master/0002.jpeg',
          'https://raw.githubusercontent.com/nilinykh/meetup_instructions/master/0003.gif',
          'https://raw.githubusercontent.com/nilinykh/meetup_instructions/master/0004.jpeg',
          'https://raw.githubusercontent.com/nilinykh/meetup_instructions/master/0005.jpeg',
          'https://raw.githubusercontent.com/nilinykh/meetup_instructions/master/0006.jpeg']

HTML = open('./HIT_template.html', 'r').read()
QUESTION_XML = """
        <HTMLQuestion xmlns="http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2011-11-11/HTMLQuestion.xsd">
        <HTMLContent><![CDATA[{}]]></HTMLContent>
        <FrameHeight>650</FrameHeight>
        </HTMLQuestion>"""
QUESTION = QUESTION_XML.format(HTML)
Q_ATTR = {
    # Amount of assignments per HIT
    'MaxAssignments': 1,
    # How long the task is available on MTurk (1 day)
    'LifetimeInSeconds': 60*1440,
    # How much time Workers have in order to complete each task (20 minutes)
    'AssignmentDurationInSeconds': 60*20,
    # the HIT is automatically approved after this number of minutes (0.5 day)
    'AutoApprovalDelayInSeconds': 60*720,
    # The reward we offer Workers for each task
    'Reward': '0.01',
    'Title': 'image click game',
    'Keywords': 'dialogue, game',
    'Description': 'prototype for an image click game'}

def publish(number_of_hits):
    '''publish HITs with creates URLs in predefined HTML template'''
    link = insert_names_and_tokens(int(number_of_hits.HITs_number))
    for login_url in link:
        create(login_url)

def create(login_url):
    '''defining HITs' template for MTurk'''
    new_hit = aws_config.ConnectToMTurk.mturk.create_hit(
        **Q_ATTR,
        Question=QUESTION.replace('${Link}', login_url).\
        replace('${Image1}', SLIDES[0]).\
        replace('${Image2}', SLIDES[1]).\
        replace('${Image3}', SLIDES[2]).\
        replace('${Image4}', SLIDES[3]).\
        replace('${Image5}', SLIDES[4]).\
        replace('${Image6}', SLIDES[5]),
        QualificationRequirements=[
        #    {
        #        'QualificationTypeId' : '3ETJLUMS0DM8X13DGYGLAJ6V7SNU3X',
        #        'Comparator' : 'NotIn',
        #        'IntegerValues' :
        #            [
        #                6, 7, 8, 9, 10
        #            ],
        #        'ActionsGuarded' : 'PreviewAndAccept'
        #    },
        #    {
        #        'QualificationTypeId' : '00000000000000000071',
        #        'Comparator' : 'In',
        #        'LocaleValues' : [
        #            {'Country':'GB'}, {'Country':'US'},
        #            {'Country':'AU'}, {'Country':'CA'},
        #            {'Country':'IE'}
        #            ],
        #        'ActionsGuarded': 'PreviewAndAccept'
        #    },
        #    {
        #        'QualificationTypeId' : '00000000000000000040',
        #        'Comparator' : 'GreaterThanOrEqualTo',
        #        'IntegerValues' : [
        #            2000
        #            ],
        #        'ActionsGuarded': 'PreviewAndAccept'
        #    }
        ])

    RESULTS.append({
        'link': login_url,
        'hit_id': new_hit['HIT']['HITId']
    })

    print('A new HIT has been created. You can preview it here:')
    print('https://worker.mturk.com/mturk/preview?groupId=' + new_hit['HIT']['HITGroupId'])
    print('HITID = ' + new_hit['HIT']['HITId'] + ' (Use to Get Results)')

def publish_hits():
    '''publish n HITs'''
    print('Relax and wait while your HITs are being published...')
    parser_variables = argparse.ArgumentParser(description='publishing HITs')
    parser_variables.add_argument('-n', '--HITs_number',
                                  help='amount of HITs to be published',
                                  default='3')
    args = parser_variables.parse_args()
    publish(args)
    moment = time.strftime("%Y-%b-%d__%H_%M_%S", time.localtime())
    with open('./published/data_'+moment+'.json', 'w') as outfile:
        json.dump(RESULTS, outfile)

if __name__ == "__main__":
    publish_hits()
