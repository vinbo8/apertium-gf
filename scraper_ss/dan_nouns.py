# coding: utf-8
import re, subprocess
cd ~/Dev/FOSS/Apertium/apertium-dan

def make_list(lines):
    out = {}
    temp = {}
    lemma = ""
    lines = filter(lambda x: "NON_ANALYSIS" not in x, lines)
    try:
        l = map(lambda x: re.findall(r'([^:]*):([^<]*)(.*)', x)[0], lines)
    except:
        l = []
    # --
    l = filter(lambda x: "<n>" in x[2] and "<nom>" in x[2], l)
       
    for i in l:
        if lemma != i[1]:
            if len(temp) == 4:
                out[lemma] = temp
            lemma = i[1]
            temp = {}
        if "<sg>" in i[2] and "<ind>" in i[2]:    
            temp["sg.ind"] = i[0]
        if "<sg>" in i[2] and "<def>" in i[2]:    
            temp["sg.def"] = i[0]
        if "<pl>" in i[2] and "<ind>" in i[2]:
            temp["pl.ind"] = i[0]
        if "<pl>" in i[2] and "<def>" in i[2]:
            temp["pl.def"] = i[0]       
    # --
  
    return out 

def ap_translate(words):
    f = open("word_dump", "w")
    for i in words:
        f.write("%s.\n" % i[1])
    f.close()    
    
    # --
    subprocess.check_output('cat word_dump | apertium -d . swe-dan > tr_dump', shell=True)
    # --
    
    f = open("tr_dump", "r")
    l = f.readlines()
    f.close()

    return zip(map(lambda x: x[0], words), l)

f = open("expanded.dix")
lines = f.read().split("\n")
f.close()

# --
w = make_list(filter(lambda x: "<n>" in x, lines))
# --


cd ~/Dev/FOSS/GF-master/lib/src/translator/


lins = open("DictionarySwe.gf").read().split("\n")


# --
words = map(lambda x: x[0], filter(lambda x: len(x) != 0, map(lambda x: re.findall(r'lin (\w*_N) = mkN "(\w*)"', x), lins)))
# --

cd ~/Dev/FOSS/Apertium/apertium-swe-dan

out = []

for i in ap_translate(words):
    ron = i[1]
    if ron.startswith("*"):
        out.append("*FAIL %s" % i[0])
        continue
    ron = ron.lstrip("#").rstrip(".\n")
    if ron in w:
        # --
        out.append("lin %s = mkN \"%s\" \"%s\" \"%s\" \"%s\" ;" % (i[0], w[ron]["sg.ind"], w[ron]["sg.def"], w[ron]["pl.ind"], w[ron]["pl.def"]))
        # --
    else:
        out.append("#FAIL %s = %s" % (i[0], ron))



l = filter(lambda x: "FAIL" not in x,  out)

cd ~/Dev/FOSS/GF-master/lib/src/translator/

print l


