
# -*- coding: utf-8 -*-
import re
import random
#---------------------------------------------------------------------------------------#
#                     Data Structures
#---------------------------------------------------------------------------------------#

labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
label_2_int = {'A':0, 'B':1, 'C':2, 'D':3, 'E':4, 'F':5, 'G':6}

closing_type_names = {
    'v':'考查动词', 'n':'考查名词',
    'adj':'考查形容词', 'adv':'考查副词', 
    'group':'考查词组', 'join':'考查衔接词'
}

type_names = {
    'info':'细节信息题', 'com':'细节综合题', 'vip':'人物观点题', 
    'wd':'词义题', 'eg':'例证题', 'infer':'推断题',
    'att':'作者态度题', 'pp':'文章主旨题'}
class objectview():
    def __init__(self, d):
        self.__dict__ = d

def split_article_stce(article):
    paragraphs = []
    for para in article:
        stces = re.split(r"\s*\/\d*\/\s*", para)
        # stces = list(map(trim, stces))
        paragraphs.append(stces)
    return paragraphs
    
class Meta(dict):
    def __init__(self):
        pass
        
    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            raise AttributeError("No such attribute: " + name)
    
    def __setattr__(self, name, value):
        self[name] = value
    
    def __delattr__(self, name):
        if name in self:
            del self[name]
        else:
            raise AttributeError("No such attribute: " + name)
    
    #@classmethod
    def from_string(self, meta_string):
        for info in meta_string.split('\n'):
            #print(info)
            m = re.match(r'(.*)=(\s*\{.*)', info)
            if m:
                item = m.group(1).strip()
                #print(m.group(2))
                try:
                    m = re.match(r'\{(.*)\}', m.group(2).strip())
                    value = m.group(1).strip()
                except:
                    print('Failed read meta from string: ' + meta_string)
                    raise
                else:
                    try:
                        value
                    except:
                        raise
                    else:
                        self[item] = value
            else:
                m = re.match(r'\@online\{(.*)\,', info)
                if m:
                    self.filename = m.group(1).strip()

class PartArticle:      # one part of the article that is necessary to solve the Question.
    def __init__(self):
        self.scope = ''      # scope of the part. 'S' for sentence or 'P' for paragraph
        self.para = -1      # the paragraph number of the article.
        self.stce = -1  # the sentence number of the article.
        self.continuous = 'IC'    # is it continuous with previous article part.
                                   # 'IC':continuous in the same para; 'DC' continuous but different para. 
                                   # 'IG': gap within para; 'DG': gap between different para
        self.text = []
        self.trans = []
    
class Position:
    def __init__(self):
        self.scope = ''  # scope of the question; 'S' for sentence or 'P' for paragraph
        self.para = -1  # the solution paragraph
        self.stce = -1   # the solution sentence
        self.related_parts = [] # the related parts of the article necessary to solve the question.
        
    def add_parts(self, article_st, translation_st, stri):
        positions = re.split(r'\s*\;\s*', stri)  # stri is like: P1S2;P2;P3
        for pos_this in positions:
            pa = PartArticle()
                
            (last_para, last_stce, last_stce_total) = (-1, -1, -1)  # location of last related part.
            (expected_para, expected_stce) = (-1, -1)               # expected position of next part, to calculated if there is a gap.
            if len(self.related_parts) != 0:
                (last_para, last_stce) = (self.related_parts[-1].para, self.related_parts[-1].stce)
                last_stce_total = len(article_st[last_para-1])
                if last_stce == -1:    # meaning that last related part is a full paragraph.
                    (expected_para, expected_stce) = (last_para+1, 1)
                elif last_stce == last_stce_total:    # meaning that last part reaches the end of its paragraph
                    (expected_para, expected_stce) = (last_para+1, 1)
                else:
                    (expected_para, expected_stce) = (last_para, last_stce+1)
                
            m = re.match(r'P(\d+)S(\d+)', pos_this)
            if m:
                pa.scope = 'S'
                pa.para = int(m.group(1))
                pa.stce = int(m.group(2))
                    
                if expected_para != -1:
                    if (pa.para, pa.stce) == (expected_para, expected_stce):
                        if pa.stce != 1:
                            pa.continuous = 'IC'    # continuous within the same paragraph.
                        else:
                            pa.continuous = 'DC'    # continuous but begin new paragraph (DC = differen para).
                    else:
                        if pa.para == last_para:
                            pa.continuous = 'IG'    # gap within paragraph
                        else:
                            pa.continuous = 'DG'    # gap outside paragraph
                    
                try:
                    #pa.text = article_st[pa.para-1][pa.stce-1]
                    pa.text = [article_st[pa.para-1][pa.stce-1]]
                    if len(translation_st[pa.para-1]) >= pa.stce:  # to handle fake translation like '>译文' in the article.
                        pa.trans = [translation_st[pa.para-1][pa.stce-1]]
                    #print(pa.para, pa.stce, pa.continuous)
                except:
                    print('Position.add_parts: position out of article boundry')
                    #print(str)
                    #print(article_st)
                    
            else:
                m = re.match(r'P(\d+)', pos_this)
                if m:
                    pa.scope = 'P'
                    pa.para = int(m.group(1))
                       
                    if expected_para != -1:    # has a previous part
                        if pa.para == expected_para:
                            pa.continuous = 'DC'    # continuous but begin new paragraph
                        else:
                            pa.continuous = 'DG'    # gap outside paragraph
                    else:    # has no previous part. 
                        pa.continuous = 'DC'
                    
                    try:
                        #pa.text = ' '.join(article_st[pa.para-1])
                        pa.text = article_st[pa.para-1]
                        if len(translation_st) >= pa.para:
                            pa.trans = translation_st[pa.para-1]
                        #print(pa.para, pa.stce, pa.continuous)
                    except:
                        print('Position.add_parts: position out of article boundry')
                
            self.related_parts.append(pa)
        

class QC:    # Question of Closing
    def __init__(self):
        self.idx = -1
        self.type = ''
        self.type_cn = ''    # Chinese name of type.
        self.location = ''
        self.position = Position()
        self.A = ['', '']
        self.B = ['', '']
        self.C = ['', '']
        self.D = ['', '']
        self.answer = 'X'     # A, B, C or D
        
        self.exp = ''
        self.meani = ''
        self.group = ''
        self.logic = ''
        self.gramm = ''
    
    def parse_position(self, article_st, translation_st, pos_str):
        self.location = pos_str
        pos = Position()
        m = re.match(r'\~', pos_str)  # to not print certain questions identified by ~, like ~P4S2;P4S3
        if m:
            pass
        else:
            pos.add_parts(article_st, translation_st, pos_str)
            self.position = pos
        
    def get_option(self, label):
        if label == 'A':
            return self.A
        elif label == 'B':
            return self.B
        elif label == 'C':
            return self.C
        elif label == 'D':
            return self.D
        
        
class Closing:
    def __init__(self):
        self.meta = Meta()
        self.article = []
        self.translation = []
        self.article_st = []
        self.translation_st = []
        self.Q = []    # 20 QC() objects.
        
    def split_sentence(self):
        self.article_st = split_article_stce(self.article)
        self.translation_st = split_article_stce(self.translation)
    
    def parse_question_position(self):
        for q in self.Q:
            q.parse_position(self.article_st, self.translation_st, q.location)


class QA:    # Question of Part A
    def __init__(self):
        self.type = ''
        self.type_cn = ''    # Chinese name of type.
        self.location = ''
        self.position = Position()
        self.question = ['', '', '']
        self.A = ['', '', '']
        self.B = ['', '', '']
        self.C = ['', '', '']
        self.D = ['', '', '']
        self.answer = 'X'     # A, B, C or D
    
    def shuffle(self, shuff=None):
        if shuff == None:
            shuff = [0, 1, 2, 3]
            random.shuffle(shuff)
        #print(shuff)
        options = [self.A, self.B, self.C, self.D]
        new_options = [None] * 4
        
        for i in range(0, 4):
            new_options[shuff[i]] = options[i]
            
        [self.A, self.B, self.C, self.D] = new_options
        self.answer = labels[shuff[0]]
    
    def parse_position(self, article_st, translation_st, pos_str):   #P1S2-P1S2;P2;P3
        self.location = pos_str
        pos = Position()
        pos_array = re.split(r'\s*\-\s*', pos_str)
        if len(pos_array) == 1:  # as P1S2 -- in this case, no parts are added through pos.add_parts()
            m = re.match(r'P(\d+)S(\d+)', pos_array[0])
            if m:
                pos.scope = 'S'
                pos.para = int(m.group(1))
                pos.stce = int(m.group(2))
            else:
                m = re.match(r'P(\d+)', pos_array[0])
                if m:
                    pos.scope = 'P'
                    pos.para = m.group(1)
        elif len(pos_array) == 2:   # as: P1S2-P1S2;P2;P3
            m = re.match(r'P(\d+)S(\d+)', pos_array[0])  #like: P1S2
            if m:
                pos.scope = 'S'
                pos.para = int(m.group(1))
                pos.stce = int(m.group(2))
            else:
                m = re.match(r'P(\d+)', pos_array[0])
                if m:
                    pos.scope = 'P'
                    pos.para = m.group(1)
            pos.add_parts(article_st, translation_st, pos_array[1])
            
        else:
            print('Wrong type of string: {}'.format(pos_str))
        
        self.position = pos
    
        
class PartA:
    def __init__(self):
        self.meta = Meta()
        #self.meta.from_string(meta_string)
        self.article = []
        self.translation = []
        self.article_st = []
        self.translation_st = []
        self.Q = [QA(), QA(), QA(), QA(), QA()]
        
    def split_sentence(self):
        self.article_st = split_article_stce(self.article)
        self.translation_st = split_article_stce(self.translation)
    
    def parse_question_position(self):
        for q in self.Q:
            q.parse_position(self.article_st, self.translation_st, q.location)
    
class PartB:
    def __init__(self):
        self.meta = Meta()
        
        self.article = []
        self.article_st = []
        
        self.translation = []
        self.translation_st = []
        
        self.characters = ['', '', '', '', '']      # useless if PartB2
        self.opinions = [['', ''], ['', ''], ['', ''], ['', ''], ['', ''], ['', ''], ['', '']]  # used as opinions in PartB2 and as titles in PartB2
        
        self.intpts = [['', ''], ['', ''], ['', ''], ['', ''], ['', '']]  # [[interpretation, interference]]
        self.no_intf = []    # interpretations of false options that does not interfere with right options
        self.opinions_order = 'ABCDEFG'
        self.answers = ['A', 'B', 'C', 'D', 'E']
    
    def split_sentence(self):
        self.article_st = split_article_stce(self.article)
        self.translation_st = split_article_stce(self.translation)
    
    def shuffle(self, shuff=None, shuff_str=None):
        
        if shuff_str is not None:
            shuff = [label_2_int[item] for item in list(self.opinions_order)]
        
        if shuff is None:
            shuff = [0, 1, 2, 3, 4, 5, 6]
            random.shuffle(shuff)
        new_opinions = [None] * 7
        
        for i in range(0, 7):
            new_opinions[shuff[i]] = self.opinions[i]
            
        self.opinions = new_opinions
        self.answers = [labels[shuff[i]] for i in range(0, 5)]
     
     
class TslAnalysis:
    def __init__(self):
        self.para_idx = -1
        self.stce_idx = -1
        self.sentence = ''
        self.trans = ''
        
        self.wd_meaning = ''
        self.wd_add = ''
        self.wd_cut = ''
        self.wd_convert = ''
        
        self.st_adjust = ''
        self.st_convert = ''
        self.st_split = ''
        self.st_combine = ''

class Tsl:
    def __init__(self):
        self.meta = Meta()
        
        self.article = []
        self.article_st = []
        
        self.translation = []
        self.translation_st = []
        
        self.analysis = []
        
    def split_sentence(self):
        self.article_st = split_article_stce(self.article)
        self.translation_st = split_article_stce(self.translation)

class Writing:
    def __init__(self):
        self.meta = Meta()
        self.l_direction = []    # l for letter OR little
        self.l_explanation = []
        self.l_model = []
        self.l_translation = []
        self.e_direction = []    # e for essay
        self.e_data = []
        self.e_explanation = []
        self.e_model = []
        self.e_translation = []
        
    
class Paper:
    # closing = 
    def __init__(self):
        self.cosing = Closing()
        self.partA = [PartA(), PartA(), PartA(), PartA()]
        self.partB = PartB()
        self.tsl = Tsl()
        self.writing = Writing()

def answer_shuff():
    # in order to generate answers for PartA so that their are equal numbers of A, B, C, and Ds
    # also to ensure that in each run the random answers stay the same
    answerA = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3]
    random.shuffle(answerA)
    answer_shuff = []
    for i in range(0, 20):
        shuff = []
        shuff.append(answerA[i])
        shuff_tail = []
        for j in range(0, 4):
            if j != answerA[i]:
                shuff_tail.append(j)
        random.shuffle(shuff_tail)
        shuff = shuff + shuff_tail
        answer_shuff.append(shuff)
    print("answer_shuff = ", answer_shuff)
    return answer_shuff
#print(answer_shuff)




