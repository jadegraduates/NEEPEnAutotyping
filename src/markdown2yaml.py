

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
        
def markdown_to_yaml(paper_files):
    # paper = Paper()
    paper = Paper_temp()

    if 'Closing' in paper_files:
        paper.closing = readClosing(paper_files['Closing'])
        for i in range(0, len(paper.closing.article)):
            paper.closing.article[i] = trim(paper.closing.article[i])
            paper.closing.translation[i] = trim(paper.closing.translation[i])
        paper.closing.article_st = None
        paper.closing.translation_st = None
        for q in paper.closing.Q:
            q.idx = int(q.idx)
            q.position = None
        
        with open(os.path.splitext(paper_files['Closing'])[0] + '.yaml', "w") as f:
            yaml.dump(paper.closing, f, default_flow_style=False, allow_unicode=True, Dumper=NoAliasDumper, sort_keys=False, indent=4, width=10000)


    # paper.partA = [readPartA(file) for file in [paper_files['PartA1'], paper_files['PartA2'], paper_files['PartA3'], paper_files['PartA4']]]
    for i in range(1, 5):
        if 'PartA' + str(i) in paper_files:
            # print(paper_files['PartA'+str(i)])
            partA = readPartA(paper_files['PartA'+str(i)])
            # print(partA.meta.author)
            for j in range(0, len(partA.article)):
                partA.article[j] = trim(partA.article[j])
                partA.translation[j] = trim(partA.translation[j])
            partA.article_st = None
            partA.translation_st = None
            for q in partA.Q:
                q.position = None
                for k in range(0, 3):
                    q.question[k] = trim(q.question[k])
                    q.A[0] = trim(q.A[0])
                    q.B[0] = trim(q.B[0])
                    q.C[0] = trim(q.C[0])
                    q.D[0] = trim(q.D[0])
            with open(os.path.splitext(paper_files['PartA'+str(i)])[0] + '.yaml', "w") as f:
                yaml.dump(partA, f, default_flow_style=False, allow_unicode=True, Dumper=NoAliasDumper, sort_keys=False, indent=4, width=10000)
   

    if 'PartB' in paper_files:
        paper.partB = readPartB(paper_files['PartB'])
        for i in range(0, len(paper.partB.article)):
            paper.partB.article[i] = trim(paper.partB.article[i])
            paper.partB.translation[i] = trim(paper.partB.translation[i])
        paper.partB.article_st = None
        paper.partB.translation_st = None
        paper.partB.answers = None
        for i in range(0, 5):
            paper.partB.intpts[i][0] = trim(paper.partB.intpts[i][0])
            
        with open(os.path.splitext(paper_files['PartB'])[0] + '.yaml', "w") as f:
            yaml.dump(paper.partB, f, default_flow_style=False, allow_unicode=True, Dumper=NoAliasDumper, sort_keys=False, indent=4, width=10000)
 
    
    if 'Trans' in paper_files:
        paper.tsl = readTsl(paper_files['Trans'])
        for i in range(0, len(paper.tsl.article)):
            paper.tsl.article[i] = trim(paper.tsl.article[i])
            paper.tsl.translation[i] = trim(paper.tsl.translation[i])
        paper.tsl.article_st = None
        paper.tsl.translation_st = None
        
        with open(os.path.splitext(paper_files['Trans'])[0] + '.yaml', "w") as f:
            yaml.dump(paper.tsl, f, default_flow_style=False, allow_unicode=True, Dumper=NoAliasDumper, sort_keys=False, indent=4, width=10000)

    
    if 'Writing' in paper_files:
        paper.writing = readWriting(paper_files['Writing'])
        with open(os.path.splitext(paper_files['Writing'])[0] + '.yaml', "w") as f:
            yaml.dump(paper.writing, f, default_flow_style=False, allow_unicode=True, Dumper=NoAliasDumper, sort_keys=False, indent=4, width=10000)
    
    
    
    # with open(os.path.splitext(paper_files['Closing'])[0] + '.yaml', "w") as f:
    #     yaml.dump(paper.closing, f, default_flow_style=False, allow_unicode=True, Dumper=NoAliasDumper, sort_keys=False, indent=4, width=10000)
    
    # for i, file in zip(range(1, 5), [paper_files['PartA1'], paper_files['PartA2'], paper_files['PartA3'], paper_files['PartA4']]):
    #     with open(os.path.splitext(file)[0] + '.yaml', "w") as f:
    #         yaml.dump(paper.partA[i-1], f, default_flow_style=False, allow_unicode=True, Dumper=NoAliasDumper, sort_keys=False, indent=4, width=10000)
    
    # with open(os.path.splitext(paper_files['PartB'])[0] + '.yaml', "w") as f:
    #     yaml.dump(paper.partB, f, default_flow_style=False, allow_unicode=True, Dumper=NoAliasDumper, sort_keys=False, indent=4, width=10000)
    
    # with open(os.path.splitext(paper_files['Trans'])[0] + '.yaml', "w") as f:
    #     yaml.dump(paper.tsl, f, default_flow_style=False, allow_unicode=True, Dumper=NoAliasDumper, sort_keys=False, indent=4, width=10000)
    
    # with open(os.path.splitext(paper_files['Writing'])[0] + '.yaml', "w") as f:
    #     yaml.dump(paper.writing, f, default_flow_style=False, allow_unicode=True, Dumper=NoAliasDumper, sort_keys=False, indent=4, width=10000)
    


parser = argparse.ArgumentParser(description='Legacy source file conversion')
parser.add_argument('-d', '--directory', metavar='', required=True, help='required, directory for .md surce files')

args = parser.parse_args()
# print(args)
# exit()


source_dir = args.directory

out_folder = source_dir

paper_files = {}

try:
    paper_files['Closing'] = glob.glob(os.path.join(source_dir, '*Closing*.md'))[0]
except:
    pass
try:
    paper_files['PartA1'] = glob.glob(os.path.join(source_dir, '*Text1*.md'))[0]
except:
    pass
try:
    paper_files['PartA2'] = glob.glob(os.path.join(source_dir, '*Text2*.md'))[0]
except:
    pass
try:
    paper_files['PartA3'] = glob.glob(os.path.join(source_dir, '*Text3*.md'))[0]
except:
    pass
try:
    paper_files['PartA4'] = glob.glob(os.path.join(source_dir, '*Text4*.md'))[0]
except:
    pass
try:
    paper_files['PartB'] = glob.glob(os.path.join(source_dir, '*PartB*.md'))[0]
except:
    pass
try:
    paper_files['Trans'] = glob.glob(os.path.join(source_dir, '*Trans*.md'))[0]
except:
    pass
try:
    paper_files['Writing'] = glob.glob(os.path.join(source_dir, '*Writing*.md'))[0]
except:
    pass
    
markdown_to_yaml(paper_files)