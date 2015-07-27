# coding: utf-8

import re, subprocess


cd ~/Dev/FOSS/Apertium/apertium-es-ro/

def make_list(lines):
    out = {}
    temp = {}
    lemma = ""
    l = map(lambda x: re.findall(r'([^:]*):([^<]*)(.*)', x)[0], lines)
    l = filter(lambda x: "<n>" in x[2] and "<nom>" in x[2] and "<ind>" in x[2], l)
    for i in l:
        if lemma != i[1]:
            if len(temp) == 2:
                out[lemma] = temp
            lemma = i[1]
            temp = {}
        if "<sg>" in i[2]:    
            temp["sg"] = i[0]
        if "<pl>" in i[2]:
            temp["pl"] = i[0]
    
    #return filter(lambda x: len(x.values()[0]) == 2, out)    
    return out 

def ap_translate(words):
    f = open("word_dump", "w")
    for i in words:
        f.write("%s.\n" % i[1])

    subprocess.check_output('cat word_dump | apertium -d . es-ro > tr_dump', shell=True)

    f = open("tr_dump", "r")
    l = f.readlines()
    f.close()

    return zip(map(lambda x: x[0], words), l)

f = open("expanded.dix")
lines = f.read().split("\n")
f.close()
n_f = make_list(filter(lambda x: "<f>" in x, lines))
n_m = make_list(filter(lambda x: "<m>" in x, lines))


cd ~/Dev/FOSS/GF-master/lib/src/translator/

lins = open("DictionarySpa.gf").read().split("\n")

words = map(lambda x: x[0], filter(lambda x: len(x) != 0, map(lambda x: re.findall(r'lin (\w*_N) = mkN "(\w*)"', x), lins)))

cd ~/Dev/FOSS/Apertium/apertium-es-ro

out = []

for i in ap_translate(words):
    ron = i[1]
    if ron.startswith("*"):
        out.append("*FAIL %s" % i[0])
        continue
    ron = ron.lstrip("#").rstrip(".\n")
    if ron in n_f:
        out.append("lin %s = mkN \"%s\" \"%s\" feminine"    % (i[0], n_f[ron]["sg"], n_f[ron]["pl"]))
    if ron in n_m:
        out.append("lin %s = mkN \"%s\" \"%s\" masculine"   % (i[0], n_m[ron]["sg"], n_m[ron]["pl"]))
    else:
        out.append("#FAIL %s = %s" % (i[0], ron))

ft = filter(lambda x: "FAIL" not in x, out)

print ft
