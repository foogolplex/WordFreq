import PyPDF2
import ebooklib
from ebooklib import epub
import os
import sys
from bs4 import BeautifulSoup

blacklist = ['[document]', 'noscript', 'header', 'html', 'meta', 'head',
            'input', 'script']

def epub2html(path):
    book = epub.read_epub(path)
    chapters = []
    for i in book.get_items():
        if i.get_type() == ebooklib.ITEM_DOCUMENT:
            chapters.append(i.get_content())
    return chapters

def chap2text(chap):
    out = ''
    soup = BeautifulSoup(chap, 'html.parser')
    text = soup.find_all(text=True)
    for t in text:
        if t.parent.name not in blacklist:
            out += '{} '.format(t)
    return out

def clean_text(txt):
    output = []
    for html in txt:
        text = chap2text(html)
        output.append(text)
    return output

punc = ['“', '…', '”', '.', ',', '!', '?', '(', ')', '"', ';', '\n']
def word_freq(text):
    gstr = ''
    for x in text:
        gstr += x;
    apstr = ''
    for l in gstr:
        apstr += l
    apstr = apstr.split(' ')
    cleaned = []
    for word in apstr:
        word = word.lower()
        
        for l in word:
            if l in punc: 
                word = word.replace(l, '') 
        if word not in punc and word != '':
            cleaned.append(word)
    dic = {}
    for word in cleaned:
        if word in dic.keys():
            dic[word] += 1
        else:
            dic[word] = 1
    srted = sorted(dic.items(), key =
             lambda kv:(kv[1], kv[0]))
    srted.reverse() 
    for pair in srted:
        print(pair[0] + ': ' + str(pair[1]))

def main(path):  
    name, extension = os.path.splitext(path)

    if(extension == '.epub'): 
        chapters = epub2html(path)
        ctext = clean_text(chapters)       
        word_freq(ctext)
    elif(extension == '.pdf'):
        pass
    else:
        print("Error: Not a valid extension")

if(len(sys.argv) > 1):
    main(sys.argv[1]);
else:
    print("Error: No path given")
