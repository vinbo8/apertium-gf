import re, subprocess

# expanded apertium monodix
dixfile = open("expanded.dix")
dixdat  = dixfile.read().split("\n")
dixdat  = filter(lambda x: "<adj>" in x, dixdat)

# WARNING: very inefficient!
out = []
for i in dixdat:
    try:
        r = re.findall(r":(.*?)<", i)[0]
    except IndexError:
        continue
    out.append(filter(lambda x: ":%s<" % r in x, dixdat))

# make the whole thing a set
out = set(map(lambda x: tuple(x), out))

def form_words(l):
    forms = []
    try:
        forms.append(filter(lambda x: "<adj><pst><ut><sg><ind>" in x, l)[0])
        forms.append(filter(lambda x: "<adj><pst><nt><sg><ind>" in x, l)[0])
        forms.append(filter(lambda x: "<adj><pst><un><sp><def>" in x, l)[0])
        forms.append(filter(lambda x: "<adj><comp><un><sp>" in x, l)[0])
        forms.append(filter(lambda x: "<adj><sup><un><sp><ind>" in x, l)[0])
        return map(lambda x: re.findall(r"^(.*?):", x)[0], forms)
    except IndexError:
        pass

dan_words = filter(lambda x: x, map(form_words, out))

# open GF dictionary
f = open("DictionarySwe.gf")
dictdat = f.read().split("\n")
dictdat = filter(lambda x: "_A " in x and "variants" not in x, filter(lambda x: x.startswith("lin"), dictdat))

words = map(lambda x: x[0], filter(lambda x: len(x) > 0, map(lambda x: re.findall(r'lin (.*?) = mkA "(.*?)"', x), dictdat)))
twords = map(lambda x: (x[0], subprocess.check_output('echo "%s" | apertium -d . swe-dan' % x[1], shell=True)), words[:100]) 
fin_words = map(lambda x: (x[0], x[1].lstrip("#").rstrip("\n")), filter(lambda x: not x[1].startswith('*'), twords))

out_sets = []
for i in fin_words:
    for j in dan_words:
        if i[1] in j:
            out_sets.append('lin {0} = mkA "{1}" "{2}" "{3}" "{4}" "{5}"'.format(i[0], *j))
