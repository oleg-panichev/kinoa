import datetime
from distutils import dir_util
import os
import pandas as pd
import shutil
import warnings


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


def save(files, experiment_name='', params={}, scores={}, other={}, 
         comments='', update_html_flag=False, working_dir='', 
         kinoa_dir_name='__kinoa__', use_spaces=False, 
         sort_log_by='experiment_datetime', sort_log_ascending=True, 
         columns_order=[]):
    '''
    Function to save experiment.
    
    Inputs:
        - files (list of str) - List of files and directories to save.
        - experiment_name (str) - String with name of an experiment. If empty - date and time used 
          to define the name in a format %Y-%m-%d_%H-%M-%S.
        - params (dict) - Dictionary with parameters of experiment.
        - scores (dict) - Dictionary with evaluation results.
        - other (dict) - Dictionary with other data needed in log.
        - comments (str) - String with comments to the experiment.
        - working_dir (str) - Path to the directory, where log of experiments will be stored. kinoa_dir_name directory
          will be created within working_dir.
        - kinoa_dir_name (str) - Name of the directory, where logs will be stored.
        - use_spaces (bool) - Flag if spaces should be used in a directory name for current experiment.
        - sort_log_by (str or list of str) - Specify which columns to use to sort rows in the log
          file.
        - sort_log_ascending (bool or list of bool) - Sort ascending vs. descending. Specify list
          for multiple sort orders. If this is a list of bools, must match the length of the 
          sort_log_by.
        - columns_order (list of str or dict in format ('col_name': index)) - Specify order of 
          columns in the log file. Columns that are not present in columns_order will remain in the 
          file, but after specified columns.
    '''

    # Get date time of experiment log
    now = datetime.datetime.now()
    experiment_datetime = str(now.strftime('%Y-%m-%d_%H-%M-%S'))
    if len(experiment_name) == 0:
        experiment_name = experiment_datetime

    # Define delimiter for new directories
    if use_spaces:
        delimiter = ' '
    else:
        delimiter = '_'
        experiment_name = experiment_name.replace(' ', delimiter)

    # Define directory name for current experiment
    if len(working_dir) == 0:
        if experiment_name == experiment_datetime:
            working_dir = os.path.join(kinoa_dir_name, experiment_datetime)
        else:
            working_dir = os.path.join(kinoa_dir_name, experiment_datetime +
                                   delimiter + experiment_name)            
    else:
        if experiment_name == experiment_datetime:
            working_dir = os.path.join(working_dir, kinoa_dir_name, experiment_datetime)
        else:
            working_dir = os.path.join(working_dir, kinoa_dir_name, experiment_datetime +
                                   delimiter + experiment_name)            

    if not os.path.exists(working_dir):
        os.makedirs(working_dir)

    # Copy files and directories
    if isinstance(files, list):
        for file in files:
            # print(file)
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
    header_cols = ['experiment_datetime', 'experiment_name', 'comments']

    # Update dictionaries
    params_cols = []
    for k in params.keys():
        col_name = 'params.' + str(k)
        experiment_dict[col_name] = params[k]
        params_cols.append(col_name)

    scores_cols = []
    for k in scores.keys():
        col_name = 'scores.' + str(k)
        experiment_dict['scores.' + str(k)] = scores[k]
        scores_cols.append(col_name)

    other_cols = []
    for k in other.keys():
        col_name = 'other.' + str(k)
        experiment_dict['other.' + str(k)] = other[k]
        other_cols.append(col_name)

    # Append experiment to experiments log
    log_fname = os.path.join(kinoa_dir_name, 'log.csv')
    if os.path.isfile(log_fname):
        log_df = pd.read_csv(log_fname)
        existing_cols = log_df.columns
    else:
        log_df = pd.DataFrame()
        existing_cols = []

    # Update columns order in csv file
    params_cols = sorted(list(set(params_cols + [c for c in existing_cols if 'params.' in c ])))
    scores_cols = sorted(list(set(scores_cols + [c for c in existing_cols if 'scores.' in c])))
    other_cols = sorted(list(set(other_cols + [c for c in existing_cols if 'other.' in c])))
    cols_order = header_cols + params_cols + other_cols

    # Check for unknown columns
    unknown_cols = []
    for c in existing_cols:
        if c not in cols_order and c not in scores_cols:
            unknown_cols.append(c)
    cols_order += unknown_cols + scores_cols

    # Append new experiment to log
    log_df = log_df.append(pd.Series(experiment_dict), ignore_index=True)

    # Sort rows in log table
    if sort_log_by not in log_df.columns:
        warnings.warn(str(sort_log_by) + ' column was not found. Using experiment_datetime ' +
            'instead.')
        sort_log_by = experiment_datetime

    # Reorder columns using user-defined list
    if len(columns_order) > 0:
        if isinstance(columns_order, list):
            keys = list(columns_order.keys())
            for c in keys:
                if c in cols_order:
                    cols_order.remove(c)
                else:
                    warnings.warn(str(c) + ' column was not found in log. Skipped.')
                    columns_order.remove(c)
            cols_order = columns_order + cols_order

        elif isinstance(columns_order, dict):
            n_cols = len(cols_order)
            keys = list(columns_order.keys())
            for c in keys:
                if c in cols_order:
                    cols_order.remove(c)
                else:
                    warnings.warn(str(c) + ' column was not found in log. Skipped.')
                    columns_order.pop(c)

            for key, value in sorted(columns_order.items(), key=lambda x: x[1]): 
                idx = value
                if idx < 0:
                    idx = n_cols + idx + 1
                cols_order.insert(idx, key)

        else:
            warnings.warn('Wrong type of columns_order variable. List or dict is expected. ' + 
                'Got ' + str(type(columns_order)) + '.')

    # Save results to CSV file
    log_df[cols_order].sort_values(sort_log_by, ascending=sort_log_ascending).\
        to_csv(log_fname, index=False)

    if update_html_flag:
        update_html()


def update_html():
    '''
    Function to generate update report in html.
    '''
    pass
