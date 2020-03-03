import yaml
import numpy as np
import pandas as pd
import geopandas as gpd
from os import path


def get_value(data, val_token):
    '''
    Parse the token of value checking for max/min, if only a numer is given, return it,
    otherwise try to parse and cast the values. In case of not parsing identified, returns
    None, None

    returns: threshold value
             value to be replaced, if none is given, the threshold itself
    '''
    try:
        val = float(val_token)
        return val, val
    except ValueError:
        tokens = val_token.split()
        ttype = tokens[0]
        tval = tokens[1]

        val = None

        if (ttype == '%') or (ttype == 'qt') or (ttype == 'q'):
            data = np.array(data)
            qval = float(tval)
            if ttype == '%':
                qval = qval/100

            tsh = val = np.quantile(data, qval)

        else:
            return None, None

        if len(tokens) > 2:
            val = cast_data(token[2])

        return tsh, val

def cast_data(data):
    '''
    Interpret a string and check if it is a float type
    '''
    try:
        val = float(data)
    except:
        if val == 'None':
            return None
        return val


def eval_level_1(node ):
    '''
    Process the first level of the configuration file tree, each entry
    contains one file to be processed
    '''
    for k, n in node.items():
        if k == 'file':
            ftype = node.get('ftype', None)
            df, _ = handle_file(n, ftype)
        elif k == 'columns':
            df = eval_columns(n, df)
    return df


def eval_columns(node, df):
    '''
    Loop through the columns and call the eval_column for each
    '''
    for k, n in node.items():
        source = n.get('source', k)
        if n == 'drop':
            df = df.drop(columns=k)
        if n == 'drop na':
            df = df.dropna(subset=source)
        else:
            df.loc[:,k] = eval_column(n, df.loc[:,source].copy())

    return df


def eval_column(node, col):
    '''
    Check the tokens to create the column and return its values
    '''
    for k, n in node.items():
        if k == 'max value':
            tsh, val = get_value(col, n)
            col.loc[col > tsh] = val
        elif k == 'min value':
            tsh, val = get_value(col, n)
            col.loc[col < tsh] = val
        elif k == 'type':
            col.astype(n)

    return col


def handle_file(file_name, ftype=None):
    '''
    Read file containing the dataframe. If not file type is given try to infer from
    the file extention
    '''
    fpath, fname = path.split(file_name)

    if ftype == None:
        ftype = path.splitext(fname)[1]
        if len(ftype) > 1:
            ftype = ftype[1:]
        else:
            return None, (fpath, fname)

    ftype = ftype.lower()

    if (ftype == 'h5') or (ftype == 'hdf'):
        df = pd.read_hdf(file_name)
    elif (ftype == 'csv'):
        df = pd.read_csv(file_name)
    elif (ftype == 'json'):
        df = pd.read_json(file_name)
    elif (ftype == 'geojson'):
        df = gpd.read_file(file_name)
    elif (ftype == 'shp'):
        df = gpd.read_file(file_name)
    elif (ftype == 'shpz'):
        df = gpd.read_file('zip://' + file_name)

    return df, (fpath, fname)
