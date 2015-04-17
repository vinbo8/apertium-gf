f = open("apertium-en-es.es.dix")
f.close()
ap_tags = re.findall(r'<sdef n="(.*?)"', f)

def tag_features(gf_tag):
    out = {}
    for i in gf_tag:
        out['present(%s)' % i] = True
    return out

def split(arr, s):
    random.shuffle(arr)
    n = int(len(arr) * s)
    return arr[:n], arr[n:]

for i in ap_tags:
    out = {}
    tot_acc = 0
    featuresets = [(tag_features(gf), "yes" if i in ap else "no") for (ap, gf) in final_flat]
    
    for j in range(5):
        train, test = split(featuresets, 0.8)
        classifier = nltk.NaiveBayesClassifier.train(train)
        accuracy = nltk.classify.accuracy(classifier, test)
        tot_acc += accuracy
        
    tot_acc /= 5
    print "%10s => %4s => %s" % (i, len(filter(lambda x: x[1] == "yes", featuresets)), format(tot_acc, '.3f'))
    out[i] = tot_acc

# multilabel classifier
out = {}
first, second = split(final_flat, 0.8)

for i in ap_tags:
    train = [(tag_features(gf), "yes" if i in ap else "no") for (ap, gf) in first]
    classifier = nltk.NaiveBayesClassifier.train(train)

    for x, j in enumerate(second):
        if classifier.classify(tag_features(j[1])) == "yes":
            try:
                out[str(j[1])].append((i, classifier.prob_classify(tag_features(j[1])).prob('yes')))
                out[str(j[1])] = list(set(out[str(j[1])]))
            except:
                out[str(j[1])] = [(i, classifier.prob_classify(tag_features(j[1])).prob('yes'))]

for i in out:
    tags = sorted(out[i], key=lambda x: x[1], reverse=True)
    print i, tags
    
"""
       acr =>    0 => 1.000
    predet =>  136 => 0.788
     detnt =>    0 => 1.000
       loc =>   13 => 0.969
       ant =>   28 => 0.999
        al =>    0 => 1.000
       cog =>    0 => 1.000
       atn =>    0 => 1.000
       enc =>    0 => 1.000
       pro =>   11 => 0.896
        tn =>  516 => 0.889
         n =>  200 => 0.949
        np =>   28 => 0.998
       adj =>  129 => 0.945
         f =>  157 => 0.921
         m =>  717 => 0.841
        mf =>  268 => 0.918
        sg =>  929 => 0.788
        pl =>  194 => 0.769
       adv =>  466 => 0.872
    preadv =>   96 => 0.915
        pr =>  156 => 0.947
       prn =>  660 => 0.896
       rel =>   23 => 0.963
        nn =>    0 => 1.000
        an =>   23 => 0.986
        aa =>    0 => 1.000
       ind =>   11 => 0.837
       itg =>  153 => 0.967
       det =>  184 => 0.891
       dem =>    4 => 0.784
       def =>    7 => 0.869
    cnjcoo =>  366 => 0.911
    cnjsub =>   23 => 0.986
    cnjadv =>   62 => 0.992
        nt =>   74 => 0.760
     vbser =>   12 => 0.969
   vbhaver =>    1 => 0.859
     vblex =>  344 => 0.876
     vbmod =>   34 => 0.969
       inf =>   25 => 0.992
       ger =>    4 => 0.921
        pp =>   74 => 0.941
       pri =>  203 => 0.770
        p1 =>   94 => 0.937
        p2 =>  186 => 0.730
        p3 =>  224 => 0.718
       pii =>    0 => 1.000
       ifi =>    0 => 1.000
       fti =>    0 => 1.000
       cni =>    0 => 1.000
       prs =>   42 => 0.967
       pis =>    0 => 1.000
       fts =>    0 => 1.000
       imp =>  206 => 0.830
       pos =>    0 => 1.000
        sp =>  229 => 0.754
       ref =>   38 => 0.984
       sup =>    0 => 1.000
       ord =>    0 => 1.000
       qnt =>   81 => 0.919
       num =>   52 => 0.996
      pron =>   16 => 0.876
        ij =>    0 => 1.000
      sent =>    0 => 1.000
        cm =>    5 => 0.848
      lpar =>    0 => 1.000
      rpar =>    0 => 1.000
    lquest =>    0 => 1.000
       web =>    0 => 1.000
      apos =>    0 => 1.000
   percent =>    0 => 1.000
      time =>    0 => 1.000
      guio =>    0 => 1.000
      past =>    0 => 1.000
       sep =>    0 => 1.000
      sint =>    0 => 1.000
     email =>    0 => 1.000
       obj =>    0 => 1.000
      subj =>    0 => 1.000
      subs =>    0 => 1.000
      pprs =>    0 => 1.000
       gen =>    0 => 1.000
      vbdo =>    0 => 1.000
      comp =>    0 => 1.000
      pres =>    0 => 1.000
      vaux =>    0 => 1.000
        ND =>    0 => 1.000
        GD =>    0 => 1.000
       mon =>    0 => 1.000
"""
