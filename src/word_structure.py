
#---------------------------------------------------------------------------------------#
#                     Word Structures
#---------------------------------------------------------------------------------------#

import re

class Word:
    def __init__(self):
        self.name = ''
        self.phonetic = ''
        self.frequency = 0
        self.intpt = ''
        self.construct = ''
        self.same_roots = []
        self.syn = []
        self.ant = []
        self.year = 0
        self.para = 0

def readWords(filename):
    words_dict = {}
    with open(filename, 'r') as f:
        lines = f.readlines()

    content = ''.join(lines)

    #word_strs = re.findall(r'\n\d+\..+', content, re.DOTALL)
    word_strs = re.split(r'\n\d+\.\s*', content)
    for word_str in word_strs:
        word = Word()
        for line in word_str.split('\n'):
            
            #---word-----
            m = re.match(r'''([\w\-]+)[\+\*]?
                    \s*\[([^\[\]]+)\].+          # phonetic symbol
                    \[大纲索引\].+
                    \[词频\]\:\s*(\d+)'''
                    , line, re.UNICODE|re.X)
            if m:
                word.name = m.group(1)
                word.phonetic = m.group(2)
                word.frequency = m.group(3)
                #print(word.name, word.phonetic, word.frequency)
            else:
                m = re.match(r'''([\w\-]+)[\+\*]?.+     #   words without phonetic symbol
                        \[词频\]\:\s*(\d+)'''
                        , line, re.UNICODE|re.X)
                if m:
                    word.name = m.group(1)
                    word.frequency = m.group(2)
                    #print(word.name, word.frequency)
            
            #---intpt-----
            m = re.match(r'\s*\[释义\]\s*(.+)$', line, re.UNICODE)
            if m:
                word.intpt = m.group(1)
                #print(word.intpt)
            
            #---construct-----
            m = re.match(r'\s*\[构词\]\s*\[(.+)\]\s*$', line, re.UNICODE)
            if m:
                word.construct = m.group(1)
                #print(word.construct)
            
            #---same_roots-----
            m = re.match(r'\s*\[同根词\]\s*(.+)$', line)
            if m:
                word.same_roots = re.split(r'[\s\+\*]+', m.group(1))
                #print(word.same_roots)
            
            #---synonym-----
            m = re.match(r'\s*\[同义词\]\s*(.+)$', line)
            if m:
                word.syn = re.split(r'    ', m.group(1))
                word.syn = list(set(word.syn))      # to remove duplicates
                #print(word.syn)
            
            #---antonym-----
            m = re.match(r'\s*\[反义词\]\s*(.+)$', line)
            if m:
                word.ant = re.split(r'    ', m.group(1))
                word.ant = list(set(word.ant))      # to remove duplicates
                #print(word.ant)
        words_dict[word.name] = word

    return words_dict

#words_dict = readWords("../input/words_marked.txt")

#for key in words_dict.keys():
#    print(words_dict[key].construct)
#    pass






    