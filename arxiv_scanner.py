#! /usr/bin/env python3
# -*- coding: utf-8

import os
import re
import json
import time
import arxiv

from collections import OrderedDict
from pprint import pprint

pattern = re.compile("^\d\d\d\d.\d\d\d\d\d.pdf")
id_pattern = re.compile("\d\d\d\d.\d\d\d\d\d")
output_file = "file_descriptions.txt"
dloads = "/home/{}/downloads/".format(os.environ.get("USER"))


def scan_for_arxiv(directory, pattern):
    contents = os.listdir(directory)
    return [
         get_arxiv_number(fname) for fname in contents
             if pattern.match(fname) is not None
           ]

def get_arxiv_number(fname):
    """Assuming we're going to get a file name xxx.xxxxx.pdf that represents
    a pdf we've downloaded from arxiv. We want to return the number."""
    return os.path.splitext(fname)[0]

def get_info(uids):
    res = arxiv.query(id_list=uids)
    return [ {id_pattern.search(x.id).group() :
             OrderedDict(
             [
               ("filename", dloads + id_pattern.search(x.id).group() + ".pdf"),
               ("url", x.id),
               ("title", x.title),
               ("authors", x.authors),
               ("summary", x.summary.replace('\n',' ')),
               ("published", x.published)
             ]
    )} for x in res]

def fresh_output():
    header = "Scanned directory {} for arxiv pdfs on {}\n".format(
                dloads,
                time.strftime("%d %b %Y %H:%M:%S", time.localtime())
                )
    with open(output_file, 'w') as f:
        f.write(header)

def add_info_to_output(info):
    with open(output_file, 'a') as f:
        pprint(info, stream=f)

def write_to_json(info):
    with open('arxiv_scan.json', 'w') as f:
        json.dump(info, f)

def main():
    fresh_output()
    uids = scan_for_arxiv(dloads, pattern)
    infos = get_info(uids)
    write_to_json(infos)
    [x for x in map(add_info_to_output, infos)]

if __name__ == "__main__":
    main()
