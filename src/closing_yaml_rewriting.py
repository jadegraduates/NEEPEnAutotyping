

import re
import os
import sys
sys.path.insert(0, '../')
import zs_py as zp
import argparse
import glob

from paper_structure import labels, type_names
from paper_parse import trim
from paper_structure import Paper
from paper_parse import readClosing, readPartA, readPartB, readTsl, readWriting

# from docx_wrapper import DocxWrapper
# from docx.shared import Pt
# from docx.shared import Inches
# from docx.enum.text import WD_ALIGN_PARAGRAPH

# from nltk.corpus import wordnet as wn

# circled_number = ('① ', '② ' , '③ ', '④ ' , '⑤ ' , '⑥ ' ,'⑦ ', '⑧ ' , '⑨ ' , '⑩ ' , '⑪ ' , '⑫ ' , '⑬ ' , '⑭ ' , '⑮ ')
# circled_number_2 = ('❶ ', '❷ ' , '❸ ' , '❹ ' , '❺ ' , '❻ ' , '❼ ' , '❽ ' , '❾ ' , '➓ ' , '⓫ ' , '⓬ ' , '⓭ ' , '⓮ ' , '⓯ ' )

#---------------------------------------------------------------------------------------#
#                             Paper subs
#---------------------------------------------------------------------------------------#

import yaml

def load_from_yaml(file):
    with open(file, "r") as f:
        try:
            obj =  yaml.load(f, Loader=yaml.FullLoader)
            # obj =  yaml.safe_load(f)
        except yaml.YAMLError as exc:
            print(exc)
    return obj

class Paper_temp():
    def __init__(self):
        self.cosing = None
        self.partA = [None, None, None, None]
        self.partB = None
        self.tsl = None
        self.writing = None
    
class NoAliasDumper(yaml.Dumper):
    def ignore_aliases(self, data):
        return True
        



parser = argparse.ArgumentParser(description='Legacy source file conversion')
parser.add_argument('-d', '--directory', metavar='', required=True, help="required, directory for Closing.yaml surce file. This program concats 'group', 'logic', 'gramm', into 'exp, and dumps 'meani'")

args = parser.parse_args()
# print(args)
# exit()


source_dir = args.directory

out_folder = source_dir

paper_files = {}

try:
    paper_files['Closing'] = glob.glob(os.path.join(source_dir, '*Closing*.yaml'))[0]
except:
    pass

paper_closing = load_from_yaml(paper_files['Closing'])
for idx in range(0, 20):
    paper_closing.Q[idx].exp = paper_closing.Q[idx].exp + paper_closing.Q[idx].group + paper_closing.Q[idx].logic + paper_closing.Q[idx].gramm
    paper_closing.Q[idx].meani = ''
    paper_closing.Q[idx].group = ''
    paper_closing.Q[idx].logic = ''
    paper_closing.Q[idx].gramm = ''

with open(os.path.splitext(paper_files['Closing'])[0] + '.rewrite.yaml', "w") as f:
    yaml.dump(paper_closing, f, default_flow_style=False, allow_unicode=True, Dumper=NoAliasDumper, sort_keys=False, indent=4, width=10000)
