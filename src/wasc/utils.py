# SPDX-FileCopyrightText: 2023-present Guillaume Collet <bilouweb@free.fr>
#
# SPDX-License-Identifier: CECILL-2.1
"""
This module provides some reading functions
"""
from urllib.parse import urljoin

import pandas as pd

HEADER = {
    "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
        (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36" ,
    "referer" : "https://www.google.com/"
    }
OK = 200

def read_checkers(filename) :
    """
    Reads the list of checkers.

    Parameters
    ----------
    filename : str
        File name containing list of checkers

    Returns
    -------
    : list
        A list of checker names
    """
    with open(filename, encoding = "utf-8") as config_file :
        return [line.strip() for line in config_file]

def read_websites(filename) :
    """
    Reads the websites list, each website is a couple (label, URL)
    """
    df = pd.read_csv(filename, sep=";", comment="#", header = None, names=["org", "url"], skipinitialspace=True)
    return list(zip(df.org, df.url))

def check_and_correct_url(target_url : str, root_url : str) -> str :
    """
    This method check if the target_url is truncated and, if so,
    recompose from the root_url
    """
    return str(urljoin(root_url.strip("/"), target_url.strip("/")))

def find_link(access_tag, root_url):
    while access_tag and access_tag.name != "a" and access_tag.name != "html":
        access_tag = access_tag.parent
    try :
        return check_and_correct_url(access_tag.attrs["href"], root_url)
    except KeyError :
        pass
