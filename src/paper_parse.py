#---------------------------------------------------------------------------------------#
#                     ParseQA & readPartA
#---------------------------------------------------------------------------------------#
import re
import random
import sys
sys.path.insert(0, '../')
import zs_py as zp
from paper_structure import Paper, Closing, QC, PartA, QA, PartB, Tsl, TslAnalysis, Writing

def trim(string, spaces_only=False):
    string = string.strip()
    if not spaces_only:
        string = re.sub(r'^\>\d*\.?\s+', "", string)     # >1. paragraph text; 
        string = re.sub(r'^\>', "", string)              # >paragraph text
        string = re.sub(r'^\d+\.\s+', "", string)         # 1. the first question
        string = re.sub(r'^\d+\.\s*\[.*\]\s*', "", string)         # 23. [info] Parkrun is different
        string = re.sub(r'^\s*[ABCD]\.\s*', "", string)  # A. option
        string = re.sub(r'^\[.*\]\s*', "", string)       # [P1S2] first option
        string = re.sub(r'\s*\\_\\_', " ______", string)  #\_\_.
    string = re.sub(r'\n+\s*$', "", string)             # \n
    return string
    
def split_article_stce(article):
    paragraphs = []
    for para in article:
        stces = re.split(r"\s*\/\d*\/\s*", para)
        stces = list(map(trim, stces))
        paragraphs.append(stces)
    #print(paragraphs[2])
    return paragraphs
        
def parseQC(QC_string, article_st, translation_st):
    qC = QC()
    m = re.match(r'''
    (\d+)\.\s*\[(.+?)\]\s*   # 2, type
    (A\.\s*[^\n]+)\s*        # 3, A
    (B\.\s*[^\n]+)\s*
    (C\.\s*[^\n]+)\s*
    (D\.\s*[^\n]+)\s*
    \>\d+\.\s*(.+)\s*          # 7, explanation
    \[meani\]\s*(.*)\s*      # 8, meaning
    \[group\]\s*(.*)\s*      
    \[logic\]\s*(.*)\s*      
    \[gramm\]\s*(.*)\s*      # 11, grammar
    
    ''', QC_string, re.DOTALL|re.X)

    if m:
        qC.idx = m.group(1)
        qC.type = m.group(2)
        #print(m.group(8))
        
        qC.A[0] = trim(m.group(3))
        m_1 = re.match(r'^\s*A.\s*\[(.*)\]\s*(.+)\s*', m.group(3))
        if m_1:
            qC.answer = 'A'
            positions = m_1.group(1)
            qC.parse_position(article_st, translation_st, positions)
            #print(m_1.group(2))
        
        qC.B[0] = trim(m.group(4))
        m_1 = re.match(r'^\s*B.\s*\[(.*)\]\s*(.+)\s*', m.group(4))
        if m_1:
            qC.answer = 'B'
            positions = m_1.group(1)
            qC.parse_position(article_st, translation_st, positions)
            #print(m_1.group(2))
            
        qC.C[0] = trim(m.group(5))
        m_1 = re.match(r'^\s*C.\s*\[(.*)\]\s*(.+)\s*', m.group(5))
        if m_1:
            qC.answer = 'C'
            positions = m_1.group(1)
            qC.parse_position(article_st, translation_st, positions)
            #print(m_1.group(2))
            
        qC.D[0] = trim(m.group(6))
        m_1 = re.match(r'^\s*D.\s*\[(.*)\]\s*(.+)\s*', m.group(6))
        if m_1:
            qC.answer = 'D'
            positions = m_1.group(1)
            qC.parse_position(article_st, translation_st, positions)
            #print(m_1.group(2))
        
        qC.exp = (m.group(7).strip())
        qC.meani = (m.group(8).strip())
        qC.group = (m.group(9).strip())
        qC.logic = (m.group(10).strip())
        qC.gramm = (m.group(11).strip())
        
    return qC

def readClosing(filename):
    closing = Closing()
    with open(filename, 'r') as f_PartA:
        lines = f_PartA.readlines()
    
    lines_1 = []
    for l in lines:    # stop taking in contents at __END__ demarkation
        m = re.match(r'__END__', l)
        if m:
            break
        lines_1.append(l)

    content = ''.join(lines_1)
    #print(content)
    m = re.match(r'\s*```(.*)```\s*(.*?)(\n\d+\..+)$', content, re.DOTALL)
    if m:
        #print(m.group(3))
        try:
            meta_string = m.group(1).strip()
            article_string = m.group(2).strip()

        except:
            print('\nReading Closing from file {} failed\n'.format(filename))
    
        try:
            closing.meta.from_string(meta_string)
            #print(closing.meta)
        except:
            print('\nReading Closing META data from file {} failed\n'.format(filename))
            
        paragraphs = article_string.split('\n')
        #print(len(paragraphs))
        for i in range(0, int(len(paragraphs)/2)):
            closing.article.append(paragraphs[2*i])
            closing.translation.append(paragraphs[2*i+1])
    
        closing.article_st = split_article_stce(closing.article)
        closing.translation_st = split_article_stce(closing.translation)
        
        QC_string_20 = m.group(3).strip()
        #QC_string_array = re.findall(r'\d+\..+?gramm\]', QC_string_20, re.DOTALL)
        QC_string_array = re.findall(r'\d+\..+?gramm\][^\n]*', QC_string_20, re.DOTALL)
        
        try:
            for QC_string in QC_string_array:
                #print(QC_string, '\n\n\n;\n\n')
                qC = parseQC(QC_string, closing.article_st, closing.translation_st)
                closing.Q.append(qC)
        except:
            print('Extract Closing Question string from file {} failed.\n'.format(filename))
    else:
        print("failed to match closing file.")
        
    return closing

#closing = readClosing("../input/gaofen/1.Closing/2015-Closing-M0.md")

#print(closing.Q[19].position.related_parts[0].text)

def parseQA(QA_string, article_st, translation_st):
    qA = QA()
    #print('abc')
    m = re.match(r'''\s*(\d+\..+)\s+
        (\>\d.+)\s+
        (\>\d.+)'''
        , QA_string, re.DOTALL|re.X)
    if m:
        #print(m.group(1))
        m_1 = re.match(r'''\s*(\d+\.\s*\[(.*)\].+)
                \s*(A\..+)
                (B\..+)
                (C\..+)
                (D\..+)'''
                , m.group(1).strip(), re.DOTALL|re.X)
        if m_1:
            qA.type = m_1.group(2)
            #print(m_1.group(6))
            qA.position = m_1.group(4)
            qA.question[0] = m_1.group(1)
            
            qA.A[0] = m_1.group(3).strip()
            #qA.A[0] = trim(qA.A[0])
            
            qA.B[0] = m_1.group(4).strip()
            #qA.B[0] = trim(qA.B[0])
            
            qA.C[0] = m_1.group(5).strip()
            #qA.C[0] = trim(qA.C[0])
            
            qA.D[0] = m_1.group(6).strip()
            #qA.D[0] = trim(qA.D[0])
            
            m_2 = re.match(r'^\s*A.\s*\[(.*)\]', qA.A[0])
            if m_2:
                qA.answer = 'A'
                positions = m_2.group(1)
                qA.parse_position(article_st, translation_st, positions)
            m_2 = re.match(r'^\s*B.\s*\[(.*)\]', qA.B[0])
            if m_2:
                qA.answer = 'B'
                positions = m_2.group(1)
                qA.parse_position(article_st, translation_st, positions)
            m_2 = re.match(r'^\s*C.\s*\[(.*)\]', qA.C[0])
            if m_2:
                qA.answer = 'C'
                positions = m_2.group(1)
                qA.parse_position(article_st, translation_st, positions)
            m_2 = re.match(r'^\s*D.\s*\[(.*)\]', qA.D[0])
            if m_2:
                qA.answer = 'D'
                positions = m_2.group(1)
                qA.parse_position(article_st, translation_st, positions)
                

        
        else:
            raise Exception('QA Question')
        
        m_1 = re.match(r'''\s*\>(\d+\..+)
                \s*\>(A\.\s*.+)
                \>(B\..+)
                \>(C\..+)
                \>(D\..+)'''
                , m.group(2).strip(), re.DOTALL|re.X)
        if m_1:
            #print(m_1.group(1))
            qA.question[2] = m_1.group(1)
            qA.A[2] = m_1.group(2).strip()
            qA.A[2] = trim(qA.A[2])
            
            qA.B[2] = m_1.group(3).strip()
            qA.B[2] = trim(qA.B[2])
            
            qA.C[2] = m_1.group(4).strip()
            qA.C[2] = trim(qA.C[2])
            
            qA.D[2] = m_1.group(5).strip()
            qA.D[2] = trim(qA.D[2])
            
        else:
            raise Exception('QA Solution') 
    
        m_1 = re.match(r'''\s*\>(\d+\..+)
                \s*\>(A\.\s*.+)
                \>(B\..+)
                \>(C\..+)
                \>(D\..+)'''
                , m.group(3).strip(), re.DOTALL|re.X)
        if m_1:
            qA.question[1] = m_1.group(1)
            qA.A[1] = m_1.group(2).strip()
            qA.A[1] = trim(qA.A[1])
            
            qA.B[1] = m_1.group(3).strip()
            qA.B[1] = trim(qA.B[1])
            
            qA.C[1] = m_1.group(4).strip()
            qA.C[1] = trim(qA.C[1])
            
            qA.D[1] = m_1.group(5).strip()
            qA.D[1] = trim(qA.D[1])
        else:
            raise Exception('QA Translation') 
    else:
        print('QA sting can not be parsed.')
    #qA.shuffle()
    #print(qA.A[0])
    #print(qA.answer)
    return qA

def readPartA(filename):
    partA = PartA()
    with open(filename, 'r') as f_PartA:
        lines = f_PartA.readlines()
    
    lines_1 = []
    for l in lines:    # stop taking in contents at __END__ demarkation
        m = re.match(r'__END__', l)
        if m:
            break
        lines_1.append(l)

    content = ''.join(lines_1)
    #print(content)

    m = re.match(r'\s*```(.*)```\s*(.*)(\n\d+\..*)(\n\d+\..*)(\n\d+\..*)(\n\d+\..*)(\n\d+\..*)$', content, re.DOTALL)
    if m:
        #print(m.group(1))
        try:
            meta_string = m.group(1).strip()
            article_string = m.group(2).strip()
            QA1_string = m.group(3).strip()
            QA2_string = m.group(4).strip()
            QA3_string = m.group(5).strip()
            QA4_string = m.group(6).strip()
            QA5_string = m.group(7).strip()
        except:
            print('\nReading Part A from file {} failed\n'.format(filename))
    
        try:
            partA.meta.from_string(meta_string)
        except:
            print('\nReading Part A META data from file {} failed\n'.format(filename))
            
        paragraphs = article_string.split('\n')
        #print(len(paragraphs))
        for i in range(0, int(len(paragraphs)/2)):
            partA.article.append(paragraphs[2*i])
            partA.translation.append(paragraphs[2*i+1])
    
        partA.article_st = split_article_stce(partA.article)
        partA.translation_st = split_article_stce(partA.translation)
        #print(partA.article_st)
        
        try:
            #print(QA4_string)
            partA.Q[0] = parseQA(QA1_string, partA.article_st, partA.translation_st)
            partA.Q[1] = parseQA(QA2_string, partA.article_st, partA.translation_st)
            partA.Q[2] = parseQA(QA3_string, partA.article_st, partA.translation_st)
            partA.Q[3] = parseQA(QA4_string, partA.article_st, partA.translation_st)
            partA.Q[4] = parseQA(QA5_string, partA.article_st, partA.translation_st)
        except Exception as err:
            print('Improper Question String in {}'.format(filename))
            print('Exception: ' + repr(err))
        #print(paper.partA[0].meta.url)
        #print(paper.partA[0].Q[1].question)
    
        #print(partA.article)
        #print(partA[0].translation)
        return partA
    else:
        print('Can not parse PartA file ', filename)

#partA_1 = readPartA("../input/gaofen/2.PartA/2013-Text1-M0.md")
#paper = Paper()
#paper.partA[0] = partA_1
#print(paper.partA[0].Q[4].position.related_parts[0].text)
#print(len(paper.partA[0].Q[3].position.related_parts))

#---------------------------------------------------------------------------------------#
#                             readPartB
#---------------------------------------------------------------------------------------#

label_2_int = {'A':0, 'B':1, 'C':2, 'D':3, 'E':4, 'F':5, 'G':6}

def readPartB(filename):
    partB = PartB()
    with open(filename, 'r') as f:
        lines = f.readlines()

    content = ''.join(lines)

    m = re.match(r'''\s*```(.*)```         # 1, meta
            \s*(\>.*?)                     # 2, article
            (\|.+\|)\s*\n                  # 3, table 
            \*\*Answers\:\s*(\w+)\*\*\s*   # 4, answer
            (1\..+)'''                     # 5, interpretation
            , content, re.DOTALL|re.X)
    if m:   # senario of PartB1
        #print(m.group(5))
        try:
            meta_string = m.group(1).strip()
            article_string = m.group(2).strip()
            #print(article_string)
            table_string = m.group(3).strip()
            answer_string = m.group(4).strip()
            interpret_string = m.group(5).strip()
        except:
            print('\nReading Part B from file {} failed\n'.format(filename))
        
        try:
            partB.meta.from_string(meta_string)
        except:
            print('\nReading Part B META from file {} failed\n'.format(filename))
        
        paragraphs = article_string.split('\n')
        #print(len(paragraphs))
        for i in range(0, int(len(paragraphs)/2)):
            partB.article.append(paragraphs[2*i])
            partB.translation.append(paragraphs[2*i+1])
        
        partB.article_st = split_article_stce(partB.article)
        partB.translation_st = split_article_stce(partB.translation)        
        
        table_lines = table_string.split('\n')
        #print(table_lines[2])
        for i in range(2, 7):
            segments = table_lines[i].split('|')
            partB.characters[i-2] = segments[1].strip()
            partB.opinions[i-2] = [segments[2].strip(), segments[3].strip()]
            #print(segments[3].strip())
        for i in range(7, 9):
            segments = table_lines[i].split('|')
            partB.opinions[i-2] = [segments[2].strip(), segments[3].strip()]

        m_1 = re.match(r'''(\d+\.\s*.+?)\s*    # 1
                \[intf\](.*)\s*
                
                (\d+\.\s*.+?)\s*               # 3
                \[intf\](.*)\s*
                
                (\d+\.\s*.+?)\s*               # 5
                \[intf\](.*)\s*
                
                (\d+\.\s*.+?)\s*               # 7
                \[intf\](.*)\s*
                
                (\d+\.\s*.+?)\s*               # 9
                \[intf\]([^\[\]]*)\s*
                
                ''', interpret_string, re.DOTALL|re.X)
        #print(m_1.group(9))
        if m_1:
            try:
                partB.intpts = [[m_1.group(1), m_1.group(2)], [m_1.group(3), m_1.group(4)], [m_1.group(5), m_1.group(6)], [m_1.group(7), m_1.group(8)], [m_1.group(9), m_1.group(10)]]
                partB.intpts = [ [item[0].strip(), item[1].strip()] for item in partB.intpts]
            except:
                print('false format for partB interpretation in file {}'.format(filename))
        
        m_2 = re.findall(r'\[no\-intf\]([^\[\]]+)', interpret_string)
        if m_2:
            try:
                partB.no_intf = [item.strip() for item in m_2]
            except:
                print('false format for partB interpretation in file {}'.format(filename))
        #print(partB.no_intf)
        
        #partB.intpts = interpret_string.split('\n')
    else:   # senario of PartB2
        #m = re.match(r'''\s*```(.*)```   # meta
        #        \s*\<\!.+\-\-\>            # annotation, which is useless
        #        \s*(\>.*?)               # article, translation & titles
        #        \n\s*(1\..+)'''               # interpretation
        #        , content, re.DOTALL|re.X)
        
        m = re.match(r'''\s*```(.*)```         # 1, meta
                \s*\<\!.+\-\-\>            # annotation, which is useless
                \s*(\>.*?)                     # 2, article
                \*\*Answers\:\s*(\w+)\*\*\s*   # 3, answer
                (1\..+)'''                     # 4, interpretation
                , content, re.DOTALL|re.X)
        
        if m:   
            #print(m.group(4))
            meta_string = m.group(1).strip()
            article_string = m.group(2).strip()
            answer_string = m.group(3).strip()
            interpret_string = m.group(4).strip()
        
            partB.meta.from_string(meta_string)
        
            paragraphs = article_string.split('\n')
            #print(len(paragraphs))
            en_indicator = 0
            titles = []
            for i in range(0, len(paragraphs)):
                para = paragraphs[i]
                if re.match(r'^\s*\#\#', para):
                    m = re.match(r'\#+\s*\[\s*\d\s*\]\s*(.+?)\|(.+)', para)
                    if m:
                        titles.append([m.group(1).strip(), m.group(2).strip()])
                    if len(titles) <= 5:  # the 6th and 7th are fake titles and therefore discarded.
                        partB.article.append('##' + m.group(1).strip())
                        partB.translation.append('##' + m.group(2).strip())
                elif en_indicator%2 == 0:
                    partB.article.append(para)
                    en_indicator += 1
                else:
                    partB.translation.append(para)
                    en_indicator += 1
            partB.opinions = titles
            partB.article_st = split_article_stce(partB.article)
            partB.translation_st = split_article_stce(partB.translation)
        
            m_1 = re.match(r'''(\d+\.\s*.+?)\s*    # 1
                    \[intf\](.*)\s*
                
                    (\d+\.\s*.+?)\s*               # 3
                    \[intf\](.*)\s*
                
                    (\d+\.\s*.+?)\s*               # 5
                    \[intf\](.*)\s*
                
                    (\d+\.\s*.+?)\s*               # 7
                    \[intf\](.*)\s*
                
                    (\d+\.\s*.+?)\s*               # 9
                    \[intf\]([^\[\]]*)\s*
                
                    ''', interpret_string, re.DOTALL|re.X)
            #print(m_1.group(9))
            if m_1:
                try:
                    partB.intpts = [[m_1.group(1), m_1.group(2)], [m_1.group(3), m_1.group(4)], [m_1.group(5), m_1.group(6)], [m_1.group(7), m_1.group(8)], [m_1.group(9), m_1.group(10)]]
                    partB.intpts = [ [item[0].strip(), item[1].strip()] for item in partB.intpts]
                except:
                    print('false format for partB interpretation in file {}'.format(filename))
        
            m_2 = re.findall(r'\[no\-intf\]([^\[\]]+)', interpret_string)
            if m_2:
                try:
                    partB.no_intf = [item.strip() for item in m_2]
                except:
                    print('false format for partB interpretation in file {}'.format(filename))
            #print(partB.no_intf)
            #print(partB.intpts)
            #partB.intpts = interpret_string.split('\n')
    answer_shuff = [label_2_int[item] for item in list(answer_string)]
    #print(answer_shuff)
    partB.opinions_order = answer_string
    # partB.shuffle(answer_shuff)
    return partB
    
#partB = readPartB('data/PartB-1-M1-T1.md')
#partB.opinions[5]

# partB = readPartB('../input/en_II_paper/paper-2017/PartB1-2017-M1.md')
#partB = readPartB('../input/en_II_paper/paper-2017/PartB2-2015-M5.md')

#print(partB.meta.author)
#print(partB.intpts)

#print(len(partB.article), len(partB.translation))
#---------------------------------------------------------------------------------------#
#                             read Translation
#---------------------------------------------------------------------------------------#

def readTsl(filename):
    tsl = Tsl()
    with open(filename, 'r') as f:
        lines = f.readlines()

    content = ''.join(lines)

    m = re.match(r'''\s*```(.*)```    # meta
                 \s*(\>.*)''',        # article and translation
                 content, 
                 re.DOTALL|re.X)
    if m:
        #print(m.group(1))
        try:
            meta_string = m.group(1).strip()
            article_string = m.group(2).strip()
        except:
            print('Failed reading Translation file {}'.format(filename))
        
        
        tsl.meta.from_string(meta_string)
        
        if zp.regex(re.match, r'\s*(\>.*?)(\#\#.*)$', article_string, re.DOTALL, zp.r):
            article_string = zp.r.m.group(1)
            analysis_string = zp.r.m.group(2)
            if zp.regex(re.findall, r'''\#\#\s*([P\dS]+)\.\s*
                    ([^\n]+)\s*
                    \[trans\]\s*([^\n]+)\s*
                    ([^\#]*)
                    ''', analysis_string, re.DOTALL|re.X, zp.r):
                r1 = zp.r.m
                for analysis_tuple in r1:
                    ta = TslAnalysis()
                    
                    location = analysis_tuple[0].strip()
                    sentence = analysis_tuple[1].strip()
                    translation = analysis_tuple[2].strip()
                    analysis = analysis_tuple[3].strip()
                    
                    if zp.regex(re.match, r'(\d+)', location, 0, zp.r):
                        ta.para_idx = 1
                        ta.stce_idx = zp.r.m.group(1)
                    elif zp.regex(re.match, r'P(\d+)S(\d+)', location, 0, zp.r):
                        ta.para_idx = zp.r.m.group(1)
                        ta.stce_idx = zp.r.m.group(2)
                    
                    ta.sentence = sentence
                    ta.trans = translation
                    
                    for line in analysis.split('\n'):
                        if zp.regex(re.match, r'^\s*$', line, 0, zp.r):
                            continue
                        if zp.regex(re.match, r'\s*\[wd\-meaning\]\s*(.*)$', line, 0, zp.r):
                            
                            ta.wd_meaning = zp.r.m.group(1).strip()
                            #print(ta.wd_meaning)
                            
                        elif zp.regex(re.match, r'\s*\[wd\-add\]\s*(.*)$', line, 0, zp.r):
                        
                            ta.wd_add = zp.r.m.group(1).strip()
                            
                        elif zp.regex(re.match, r'\s*\[wd\-cut\]\s*(.*)$', line, 0, zp.r):
                        
                            ta.wd_cut = zp.r.m.group(1).strip()
                        
                        elif zp.regex(re.match, r'\s*\[wd\-convert\]\s*(.*)$', line, 0, zp.r):
                        
                            ta.wd_convert = zp.r.m.group(1).strip()
                        
                        elif zp.regex(re.match, r'\s*\[st\-adjust\]\s*(.*)$', line, 0, zp.r):
                        
                            ta.st_adjust = zp.r.m.group(1).strip()
                        
                        elif zp.regex(re.match, r'\s*\[st\-convert\]\s*(.*)$', line, 0, zp.r):
                        
                            ta.st_convert = zp.r.m.group(1).strip()
                        
                        elif zp.regex(re.match, r'\s*\[st\-split\]\s*(.*)$', line, 0, zp.r):
                        
                            ta.st_split = zp.r.m.group(1).strip()
                        
                        elif zp.regex(re.match, r'\s*\[st\-combine\]\s*(.*)$', line, 0, zp.r):
                        
                            ta.st_combine = zp.r.m.group(1).strip()
                    tsl.analysis.append(ta)
        
        paragraphs = article_string.split('\n')
        #print(len(paragraphs))
        for i in range(0, int(len(paragraphs)/2)):
            tsl.article.append(paragraphs[2*i])
            tsl.translation.append(paragraphs[2*i+1])
        
        tsl.article_st = split_article_stce(tsl.article)
        tsl.translation_st = split_article_stce(tsl.translation)
    return tsl

#tsl = readTsl('data/Tr-2017082503-M0.md')
#tsl.translation

#---------------------------------------------------------------------------------------#
#                             read Writing
#---------------------------------------------------------------------------------------#

def readWriting(filename):
    writing = Writing()
    with open(filename, 'r') as f:
        lines = f.readlines()

    content = ''.join(lines)
    #print(content)
    m = re.match(r'''\s*```(.*)```              # 1 meta
                .+
                  \#\#\s*1\.\s*Directions\:
                  (.+)                          # 2 letter direction
                  \*\*1-explanation\:?\*\*
                  (.+)                          # 3 letter explanation
                  \*\*1-model\:?\*\*
                  (.+)                          # 4 letter model letter
                  \*\*1-translation\:?\*\*
                  (.+)                          # 5 letter translation
                  \#\#\s*2\.\s*Directions\:
                  (.+?)                         # 6 essay direction
                  (\|.+)                        # 7 essay data
                  \*\*2-explanation\:?\*\*
                  (.+)                          # 8 essay explanation
                  \*\*2-model\:?\*\*
                  (.+)                          # 9 essay model essay
                  \*\*2-translation\:?\*\*
                  (.+)                          # 10 essay translation
                  ''',        # article and translation
                 content, 
                 re.DOTALL|re.X)
    if m:
        #print(m.group(10))
        try:
            meta_string = m.group(1).strip()
            letter_direction = m.group(2).strip()
            letter_explanation = m.group(3).strip()
            letter_model = m.group(4).strip()
            letter_translation = m.group(5).strip()
        
            essay_direction = m.group(6).strip()
            essay_data = m.group(7).strip()
            essay_explanation = m.group(8).strip()
            essay_model = m.group(9).strip()
            essay_translation = m.group(10).strip()
        except:
            print('Failed reading writing file {}'.format(filename))
        
        try:
            writing.meta.from_string(meta_string)
        except:
            print('Failed reading META in writing file {}'.format(filename))
        
        paragraphs = letter_direction.split('\n')      # l_direction
        for i in range(0, int(len(paragraphs))):
            writing.l_direction.append(paragraphs[i])
        
        paragraphs = letter_explanation.split('\n')    # l_explanation
        for i in range(0, int(len(paragraphs))):
            writing.l_explanation.append(paragraphs[i])
        
        paragraphs = letter_model.split('\n')          # l_model
        for i in range(0, int(len(paragraphs))):
            #if re.match(r'^\s*$', paragraphs[i]) is None:
            writing.l_model.append(paragraphs[i])
            
        paragraphs = letter_translation.split('\n')    # l_translation
        for i in range(0, int(len(paragraphs))):
            #if re.match(r'^\s*$', paragraphs[i]) is None:
            writing.l_translation.append(paragraphs[i])
        
        paragraphs = essay_direction.split('\n')      # e_direction
        for i in range(0, int(len(paragraphs))):
            writing.e_direction.append(paragraphs[i])
            
        paragraphs = essay_data.split('\n')      # e_data
        for i in range(0, int(len(paragraphs))):
            writing.e_data.append(paragraphs[i])
        
        paragraphs = essay_explanation.split('\n')    # e_explanation
        for i in range(0, int(len(paragraphs))):
            writing.e_explanation.append(paragraphs[i])
        
        paragraphs = essay_model.split('\n')          # e_model
        for i in range(0, int(len(paragraphs))):
            #if re.match(r'^\s*$', paragraphs[i]) is None:
            writing.e_model.append(paragraphs[i])
            
        paragraphs = essay_translation.split('\n')    # e_translation
        for i in range(0, int(len(paragraphs))):
            #if re.match(r'^\s*$', paragraphs[i]) is None:
            writing.e_translation.append(paragraphs[i])
    else:
        print('\nFailed matching content of Writing file {}\n'.format(filename))
        
    return writing

#writing = readWriting('data/Writing-1-M1-T1-template.md')
#writing.meta['2-type']
