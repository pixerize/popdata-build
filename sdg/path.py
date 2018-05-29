# -*- coding: utf-8 -*-
"""
Utilities for paths in sdg-indicators project

Try to use this as the central location for path related functions

@author: dashton

"""

# %% Imports and globals

import glob
import os

# Paths to raw data and metadata relative to project root
site_dir = '_site'

# %% Get the IDs by scanning the metadata directory


def extract_id(md_path):
    md = os.path.basename(md_path)
    md_id = os.path.splitext(md)[0]

    return md_id


def get_ids(root=''):
    mds = glob.glob(os.path.join(input_path(ftype='meta', root=root), '*-*.md'))
    ids = [extract_id(md) for md in mds]

    return ids


# %% From ID get input path


def input_path(inid=None, ftype='data', root='', must_work=False):
    """Return path of input data and metadata for a given ID
    
    Args:
        inid: str. Indicator ID with no extensions of paths, eg '1-1-1'.
            If it is None then return the directory path for this ftype.
        ftype: str. Which file related to this ID? One of:
            1. data: Main indicator data
            2. meta: Indicator metadata
        root: str. Directory root where data and meta directories exist.
            Default is current working directory.
        must_work: bool. Should the input file exist? Throws error if not
            found.
    """

    if(root is None):
        root = ''

    expected_ftypes = ['data', 'meta']
    if ftype not in expected_ftypes:
        raise ValueError("ftype must be on of: " + ", ".join(expected_ftypes))

    if ftype == 'data':
        path = os.path.join(root, 'data')
        if inid is not None:
            path = os.path.join(path, 'indicator_' + inid + '.csv')
    elif ftype == 'meta':
        path = os.path.join(root, 'meta')
        if inid is not None:
            path = os.path.join(path, inid + '.md')
    
    return path


# %% From ID give file path


def output_path(inid=None,  ftype='data', format='json', root='', must_work=False):
    """Convert an ID into a data, edge, headline, json, or metadata path

    Args:
        inid: str. Indicator ID with no extensions of paths, eg '1-1-1'.
            Can also be "all" for all data. If it is None then return
            the directory path for this ftype.
        ftype: str. Which file related to this ID? One of:
            1. data: Main indicator data
            2. meta: Indicator metadata
            3. edges: The edge file generated from data
            4. headline: The headline data generated from data
            5. comb: combined data and edge data
        format: str. What data type. One of:
            1. json
            2. csv
        root: str. Directory root where data and meta directories exist.
            Default is current working directory.
        must_work: bool. If True an IOError is thrown if the file is not found.

    Returns:
        path to the file. If the site_dir is set this will form the base.
    """

    if(root is None):
        root = ''

    # Check that the input makes sense
    expected_ftypes = ['data', 'meta', 'edges', 'headline', 'comb']
    if ftype not in expected_ftypes:
        raise ValueError("ftype must be on of: " + ", ".join(expected_ftypes))

    expected_formats = ['csv', 'json']
    if format not in expected_formats:
        raise ValueError("format must be on of: " + ", ".join(expected_formats))

    ext = '.csv' if format == 'csv' else '.json'
    path = os.path.join(root, site_dir, ftype)
    prefix = ''

    # Get the directory path
    if inid is None:
        f = path
    else:
        f = os.path.join(path, prefix + inid + ext)
    
    if must_work:
        if not os.path.exists(f):
            raise IOError(f + ' not found.')
    return f
