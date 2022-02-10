import re, sys, subprocess, json, os
from math import log, sqrt
from collections import OrderedDict as ordd

def count_oe(xy, x, y, N, ws):
    return [xy, x - xy, y - xy, N - x - y + xy], [x * y / N * ws, x * ((N - y) / N) ** ws, y * ((N - x) / N) ** ws, (1 - (x / N + y / N)) * N]

def mi(xy, x, y, N, ws = 1):
    return log (xy / (x * y / N * ws) , 2)

def mi3(xy, x, y, N, ws = 1):
    return log (xy ** 3/ (x * y / N * ws) , 2)

def frequency(xy, x, y, N, ws = 1):
    return xy

def ll(xy, x, y, N, ws = 1):
    o, e = count_oe (xy, x, y, N, ws)
    l = 0
    for i in [1,2]:
        for j in [1,2]:
            ind = (j - 1) + (i - 1) * 2
            x = o[ind] * log (o[ind] / float (e[ind]))
            l += x
    return 2 * l

def t_score(xy, x, y, N, ws = 1):
    o, e = count_oe (xy, x, y, N, ws)
    return (o[0] - e[0]) / sqrt (o[0])

def z_score(xy, x, y, N, ws = 1):
    o, e = count_oe (xy, x, y, N, ws)
    return (o[0] - e[0]) / sqrt (e[0])

def dice(xy, x, y, N, ws = 1):
    o, e = count_oe (xy, x, y, N, ws)
    return 2 * o[0] / float (x + y)

def loadFreq(path, cs):

    freq = {}
    count = 0.
    with open (path) as fin:
        for line in fin:
            fq, word = line.strip ().split ()
            if cs:
                word = word.lower ()
            if word in freq:
                freq[word] += int (fq)
            else:
                freq[word] = int (fq)
            count += int (fq)

    return freq, count

def process():

    sys.stderr.write ('params:\n')
    sys.stderr.write (sys.argv[1] + '\n')
    sys.stderr.write ('\nsettings:\n')
    sys.stderr.write (sys.argv[2] + '\n\n')

    AMs = (('llr', ll, '%.2f'), ('mi', mi, '%.2f'), ('t-score', t_score, '%.2f'), ('z-score', z_score, '%.2f'), ('dice', dice, '%.4f'), ('mi3', mi3, '%.2f'), ('frequency', frequency, '%d'))

    freqDir = 'resources'
    params = json.loads (sys.argv[1], encoding = 'utf8')
    if 'sort' in params:
        sort = [el[0] for el in AMs].index (params['sort']) + 1
    else:
        sort = 1
    settings = json.loads (sys.argv[2])
    
    
    query = params['primquery'] + params['secondquery']
    countBy = settings['countBy']
    threshold = settings['threshold']
    chosenAms = [am for am in AMs if am[0] in settings['ams'] and settings['ams'][am[0]]]
    leftContext = settings['leftContextSize']
    rightContext = settings['rightContextSize']
    freqPath = '../%s/freq_%s_%s.txt' % (freqDir, params['primlang'].lower (), countBy == 'lemma' and 'lemma' or 'word')
    if '%c' in params['primquery']:
        cs = True
    else:
        cs = False
    freq, N = loadFreq (freqPath, cs)

    columns = u''
    for i in range (len (chosenAms)):
        columns += u'<th class="sortable">%s</th>\n' % (chosenAms[i][0])

    command = [os.path.join (params['cwbdir'], 'cqpcl'), '-r', params['registry'], '%s; set LeftContext %d words; set RightContext %d words; show -cpos; show +lemma; %s;' % (params['corpusname'], leftContext, rightContext, query)]

    sys.stderr.write (subprocess.list2cmdline (command) + '\n\n')
    proc = subprocess.Popen (command, stdout = subprocess.PIPE)
    results = proc.communicate ()[0]
    with open ('/var/www/html/Birmingham/resources/out.txt', 'w') as fout:
        fout.write (results)

    collocates = {}
    node = u''
    for line in results.splitlines ():
        words = [el.rsplit ('/', 1)[countBy == 'lemma' and 1 or 0] for el in line.strip ().split ()]
        if not node:
            node = unicode (words[int (leftContext)], 'utf8')
            if countBy == 'lemma':
                node = node[:-1]
            else:
                node = node[1:]
        try:
            del words[int (leftContext)]
        except IndexError:
            continue
        words = list (set (words))
        for word in words:
            if not word:
                continue
            if word.lower () == 'that/in':
                word = 'that'
            if cs:
                word = word.lower ()
            if word in collocates:
                collocates[word] += 1
            else:
                collocates[word] = 1
    if cs:
        node = node.lower ()
    fa = freq[node]
    collocations = []
    for collocate, fab in [coll for coll in collocates.items () if coll[1] >= threshold]:
        if cs:
            collocate = collocate.lower ()
        try:
            fb = freq[collocate]
        except KeyError:
            continue
        tmp = [collocate]

        if fa < fab or fb < fab:
            continue
        for amName, amFoo, format in chosenAms:
            try:
                tmp.append (amFoo (fab, fa, fb, N))
            except:
                sys.stderr.write ('err: %s %f, %f, %f, %d' % (amName, fab, fa, fb, N))
                tmp.append (0)
        collocations.append (tmp)
    collocations.sort (key = lambda x: x[sort], reverse = True)
    queryRes = u''
    if leftContext > 2:
        queryRes = u'%s[]{0,%d}%s' % ('%s', leftContext - 1, params['primquery'].replace ('%', '%%'))
    elif leftContext:
        queryRes = u'%s[]?%s' % ('%s', params['primquery'].replace ('%', '%%'))
    else:
        queryRes = u'%s'
    if rightContext and leftContext:
        queryRes += u' | '
    if rightContext > 2:
        queryRes += u'%s[]{0,%d}%s' % (params['primquery'].replace ('%', '%%'), rightContext - 1, '%s')
    elif rightContext:
        queryRes += u'%s[]?%s' % (params['primquery'].replace ('%', '%%'), '%s')
    else:
        queryRes += u'%s'

    GET_dict = {u'query':  queryRes, u'langs': '-'.join (params['langs']), u'primlang': params['primlang']}
    sys.stderr.write ('qR:' + queryRes + '\n\n')


    html_output = []
    print(len (collocations))
    for ind, coll in enumerate (collocations):
        word = unicode (coll[0], 'utf8')
        ams = [chosenAms[i][2] % coll[i + 1] for i in range (len (chosenAms))]
        get_query = []
        for name, val in GET_dict.items ():
            if name == u'query':
                #sys.stderr.write (val)
                try:
                    get_query.append (u'query=' + val % (leftContext and '[%s="%s"%%c]' % (countBy, word) or u'', rightContext and '[%s="%s"%%c]' % (countBy, word) or u''))
                except:
                    sys.stderr.write (val + u' ! ' + unicode (type (val)) + u'\n')
                    raise
            else:
                get_query.append (name + '=' + val)
        return '\t'.join([word] + ams)
