import re, pprint

def to_dict(l):
    d = {}
    for i in l:
        for j in i[1:]:
            try:
                d[i[0][0]].append({'lemma': j[0], 'analyses': j[1:]})
            except:
                d[i[0][0]] = [{'lemma': j[0], 'analyses': j[1:]}]
    return d

def partition_stream(stream):
    stream = stream.split("$")[:-1]
    stream = map(lambda x: x.split("/"), stream)
    for i in stream:
        i[0] = re.sub(r"\s*\^", "", i[0]) + " "
        i[1:] = map(lambda x: re.sub("(?:><|\(|\)|<|>)", " ", x), i[1:])
    stream = map(lambda x: map(lambda y: re.split(r"\s+", y)[:-1], x), stream)
    for i in stream:
        i[1:] = map(lambda x: [tuple(x[0].split("_"))] + x[1:], i[1:])
    return to_dict(stream)

def tag_substitute(d, old, new):
    for i in d:
        for n, j in enumerate(d[i]):
			if j['lemma'][1] == old or (callable(old) and old(j['lemma'][1]) == True):
                take = j['lemma'][1]
                d[i][n]['lemma'] = d[i][n]['lemma'][0]
				if new != "!":
	                d[i][n]['analyses'].append(take)
                
    for i in d:
        for n, j in enumerate(d[i]):
            for m, k in enumerate(j['analyses']):
                if k == old or (callable(old) and old(k) == True):
					if new == "!":
						del(d[i][n]['analyses'][m])
					else:
	                    d[i][n]['analyses'][m] = new
    return d

def expand_stream(d):
    stream = ""
    for i in d.keys():
        stream += "^%s/" % i
        for k in d[i]:
            stream += "%s_%s" % (k['lemma'][0], k['lemma'][1])
            for j in k['analyses']:
                stream += "<%s>" % (j)
            stream += "/"
            stream = stream[:-1]
        stream += "$ "
    return stream

# TODO: fill this up
gf_ap = {
	lambda x: x.lower() == x : "!",
    "V2": "vblex",
    "Masc": "m",
    "VPart": "pp",
    "Pl": "pl"
}
