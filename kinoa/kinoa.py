import datetime
from distutils import dir_util
import os
import pandas as pd
import shutil

KINOA_DIR = '__kinoa__'


def copytree(src, dst, symlinks=False, ignore=None):
    '''
    Function to copy directories.
    '''

    if not os.path.exists(dst):
        os.makedirs(dst)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)


def save(files, experiment_name='', params={}, scores={}, comments='',
         update_html_flag=False, working_dir=''):
    '''
    Function to save experiment.
    
    Inputs:
        files - list of files to save or string
        experiment_name - name of experiment
        params - dictionary with experiment parameters
        scores - dictionary with scores
        comments - str with comments
        update_html_flag - flag
    '''

    # Get date time of experiment log
    now = datetime.datetime.now()
    experiment_datetime = str(now.strftime('%Y-%m-%d_%H-%M-%S'))
    if len(experiment_name) == 0:
        experiment_name = experiment_datetime

    if len(working_dir) == 0:
        if experiment_name != experiment_datetime:
            working_dir = os.path.join(KINOA_DIR, experiment_datetime +
                                   ' ' + experiment_name)
        else:
            working_dir = os.path.join(KINOA_DIR, experiment_datetime)
    else:
        if experiment_name != experiment_datetime:
            working_dir = os.path.join(working_dir, KINOA_DIR, experiment_datetime +
                                   ' ' + experiment_name)
        else:
            working_dir = os.path.join(working_dir, KINOA_DIR, experiment_datetime)

    if not os.path.exists(working_dir):
        os.makedirs(working_dir)

    # Copy files
    if isinstance(files, list):
        for file in files:
            print(file)
            if os.path.isdir(file):
                copytree(file, os.path.join(working_dir, file))
            else:
                file_dir = os.path.dirname(file)
                if len(file_dir) > 0:
                    if not os.path.exists(os.path.join(working_dir, file_dir)):
                        os.makedirs(os.path.join(working_dir, file_dir))

                shutil.copy2(file, os.path.join(working_dir, file))

    # Prepare experiment description
    experiment_dict = {
        'experiment_name': experiment_name,
        'experiment_datetime': experiment_datetime,
        'comments': comments
    }
    for k in params.keys():
        experiment_dict['params.' + str(k)] = params[k]
    for k in scores.keys():
        experiment_dict['scores.' + str(k)] = scores[k]

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
