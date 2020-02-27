import yaml
import numpy as np
import pandas as pd
import geopandas as gpd
from os import path


def get_value(data, val_token):
    try:
        return float(val_token)
    except ValueError:
        tokens = val_token.split()
        ttype = tokens[0]
        tval = tokens[1]

        if (ttype == '%') or (ttype == 'qt') or (ttype == 'q'):
            data = np.array(data)
            qval = float(tval)
            if ttype == '%':
                qval = qval/100

            return np.quantile(data, qval)


def eval_level_1(node, df):
    for k, n in node.items():
        if k == 'file':
            ftype = node.get('ftype', None)
            df, _ = handle_file(n, ftype)
        elif k == columns:
            pass

    return df


def eval_level_2(node, df):
    pass


def handle_file(file_name, ftype=None):
    fpath, fname = path.split(file_name)

    if ftype == None:
        ftype = path.splitext(fname)[1]
        if len(ftype) > 1:
            ftype = ftype[1:]
        else
            return None

    ftype = ftype.lower()

    if (ftype == 'h5') or (ftype == 'hdf'):
        df = pd.read_hdf(file_name)
    elif (ftype == 'csv'):
        df = pd.read_hdf(file_name)
    elif (ftype == 'json'):
        df = pd.read_json(file_name)
    elif (ftype == 'geojson'):
        df = gpd.read_file(file_name)
    elif (ftype == 'shp'):
        df = gpd.read_file(file_name)
    elif (ftype == 'shpz'):
        df = gpd.read_file('zip://' + file_name)

    return df
