import re, subprocess

f = open("expanded.dix")
lines = f.read().split("\n")

lines = filter(lambda x: "<n>" in x, lines)
lines = filter(lambda x: "REGEXP" not in x and "NON_ANALYSIS" not in x, lines)

ut = filter(lambda x: "<ut>" in x, lines)
nt = filter(lambda x: "<nt>" in x, lines)

nt_f = map(lambda x: re.findall(r"\w+:[^\w]*:*(\w*)<", x), nt)
ut_f = map(lambda x: re.findall(r"\w+:[^\w]*:*(\w*)<", x), ut)

nt_f  = set(map(lambda x: x[0], filter(lambda x: len(x) > 0, nt_f)))
ut_f  = set(map(lambda x: x[0], filter(lambda x: len(x) > 0, ut_f)))

f = open("nt.words", "w")
for i in nt_f:
    f.write(i)
f.close()

f = open("ut.words", "w")
for i in ut_f:
    f.write(i + "\n")
f.close()

lins = open("DictionarySwe.gf").read().split("\n")

nouns = map(lambda x: x[0], filter(lambda x: len(x) != 0, map(lambda x: re.findall(r'lin (\w*_N) = mkN "(\w*)"', x), lins)))

out = []
# WARN - huge
for i in nouns:
    dan = subprocess.check_output('echo "%s" | apertium -d . swe-dan' % i[1], shell=True)
    if dan.startswith("*"):
        out.append("*FAIL %s" % i[0])
        continue
    dan = dan.lstrip("#").rstrip("\n")
    if dan in nt_f:
        out.append("lin %s = mkN \"%s\" neutrum" % (i[0], dan))
    if dan in ut_f:
        out.append("lin %s = mkN \"%s\" utrum"   % (i[0], dan))
    else:
        out.append("#FAIL %s = %s" % (i[0], dan))

