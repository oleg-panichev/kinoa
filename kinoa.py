import datetime
from distutils import dir_util
import os
import pandas as pd
import shutil

KINOA_DIR = '__kinoa__'

def save(files, experiment_name='', scores={}, comments='', 
    update_html_flag=True):
    '''
    Inputs:
        files - list of files to save or string
        experiment_name - name of experiment
        scores - dictionary with scores
        comments - str with comments
    '''

    # Get date time of experiment log
    now = datetime.datetime.now()
    experiment_datetime = str(now.strftime('%Y-%m-%d_%H-%M-%S'))
    if len(experiment_name) == 0:
        experiment_name = experiment_datetime

    working_dir = os.path.join(KINOA_DIR, experiment_datetime + 
        ' ' + experiment_name)
    if not os.path.exists(working_dir):
        os.makedirs(working_dir)

    # Copy files
    if isinstance(files, list):
        for file in files:
            # if os.path.isfile(file):
            #     src = file
            #     dst = os.path.join(KINOA_DIR, file.split())
            #     dir_util.copy_tree(file, )
            # print(file, os.path.join(KINOA_DIR, file))
            shutil.copy(file, os.path.join(working_dir, file))

    # Prepare experiment description
    experiment_dict = {
        'experiment_name': experiment_name, 
        'experiment_datetime': experiment_datetime,
        'comments': comments
    }
    for k in scores.keys():
        experiment_dict[k] = scores[k]

    # Append experiment to experiments log
    log_fname = os.path.join(KINOA_DIR, 'log.csv')
    if os.path.isfile(log_fname):
        log_df = pd.read_csv(log_fname)
    else:
        log_df = pd.DataFrame()

    log_df = log_df.append(pd.Series(experiment_dict), ignore_index=True)
    log_df.to_csv(log_fname, index=False)

    if update_html_flag:
        update_html()


def update_html():
    '''
    Function to generate update report in html.
    '''
    pass

