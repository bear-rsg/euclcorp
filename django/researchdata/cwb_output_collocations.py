import os
from math import log, sqrt
from collections import defaultdict


def count_oe(xy, x, y, N, ws):
    """
    Counts OE, which is used in various calculate functions below
    """
    return [xy, x - xy, y - xy, N - x - y + xy],\
           [x * y / N * ws, x * ((N - y) / N) ** ws, y * ((N - x) / N) ** ws, (1 - (x / N + y / N)) * N]


def mi(xy, x, y, N, ws=1):
    """
    Calculate mutual information (MI) score
    """

    return log(xy / (x * y / N * ws), 2)


def mi3(xy, x, y, N, ws=1):
    """
    Calculate mutual information (MI3) score
    """

    return log(xy ** 3 / (x * y / N * ws), 2)


def llr(xy, x, y, N, ws=1):
    """
    Calculate the log-likelihood ratio
    """

    o, e = count_oe(xy, x, y, N, ws)
    llr = 0
    for i in [1, 2]:
        for j in [1, 2]:
            ind = (j - 1) + (i - 1) * 2
            x = o[ind] * log(o[ind] / float(e[ind]))
            llr += x
    return 2 * llr


def t_score(xy, x, y, N, ws=1):
    """
    Calculate t-score
    """

    o, e = count_oe(xy, x, y, N, ws)
    return(o[0] - e[0]) / sqrt(o[0])


def z_score(xy, x, y, N, ws=1):
    """
    Calculate z-score
    """

    o, e = count_oe(xy, x, y, N, ws)
    return(o[0] - e[0]) / sqrt(e[0])


def dice(xy, x, y, N, ws=1):
    """
    Calculate dice
    """

    o, e = count_oe(xy, x, y, N, ws)
    return 2 * o[0] / float(x + y)


def frequency(xy, x, y, N, ws=1):
    """
    Calculate frequency
    """

    return xy


def loadFreq(path, case_insensitive):
    """
    Load the frequencies and counts from text file
    """

    freq = {}
    count = 0.
    with open(path) as fin:
        for line in fin:
            fq, word = line.strip().split()
            if case_insensitive:
                word = word.lower()
            if word in freq:
                freq[word] += int(fq)
            else:
                freq[word] = int(fq)
            count += int(fq)
    return freq, count


def process(cwb_query, cwb_output, options):
    """
    Takes cwb_output (the string output generated by CWB) and processes it
    to turn into a proper data format suitable for consumption in a Django template
    """

    # Ensure the output from cwb is a string
    results = str(cwb_output)

    # Stats (the various statistical outputs to include, e.g. t-score, log-likelihood ratio, etc.)
    stats = (
        ('llr', llr, '%.2f'),
        ('mi', mi, '%.2f'),
        ('t-score', t_score, '%.2f'),
        ('z-score', z_score, '%.2f'),
        ('dice', dice, '%.4f'),
        ('mi3', mi3, '%.2f'),
        ('frequency', frequency, '%d')
    )
    if 'sort' in options:
        sort = [el[0] for el in stats].index(options['sort']) + 1
    else:
        sort = 1
    chosen_stats = [stat for stat in stats if stat[0] in options['chosen_stats']]

    # Case-sensitivity
    case_insensitive = True if '%c' in cwb_query else False

    # Frequency
    module_dir = os.path.dirname(__file__)
    freq_path = os.path.join(module_dir, 'freq_birm_eng_word.txt')
    freq, N = loadFreq(freq_path, case_insensitive)

    # Build collocates dict
    collocates = defaultdict(int)  # sets default value to 0 for all objects added to dict
    node = ''
    for line in results.splitlines():
        words = [el.rsplit('/', 1)[options['countby'] == 'lemma' and 1 or 0] for el in line.strip().split()]
        if not node:
            node = str(words[options['spanleft']])
            if options['countby'] == 'lemma':
                node = node[:-1]
            else:
                node = node[1:]
        try:
            del words[int(options['spanleft'])]
        except IndexError:
            continue
        words = list(set(words))
        for word in words:
            if not word:
                continue
            if word.lower() == 'that/in':
                word = 'that'
            if case_insensitive:
                word = word.lower()
            collocates[word] += 1

    # Case sensitivity
    if case_insensitive:
        node = node.lower()

    # Build collocations list
    fa = freq[node]
    collocations = []
    for collocate, fab in [coll for coll in collocates.items() if coll[1] >= options['threshold']]:
        if case_insensitive:
            collocate = collocate.lower()
        try:
            fb = freq[collocate]
        except KeyError:
            continue
        tmp = [collocate]
        if fa < fab or fb < fab:
            continue
        for stat_name, stat_foo, format in chosen_stats:
            try:
                tmp.append(stat_foo(fab, fa, fb, N))
            except Exception:
                pass
        collocations.append(tmp)
    collocations.sort(key=lambda x: x[sort], reverse=True)

    # Build collocations output data rows
    collocation_output_data = []
    for ind, coll in enumerate(collocations):
        # Build a row to show in output table.
        row = {'word': str(coll[0])}
        # E.g. {'word': 'the', 'llr': '33850.44', 't-score': '85.22', 'dice': '0.0043', 'mi3': '29.48'}
        # Append each chosen statistic to the row dict
        for i, stat in enumerate(chosen_stats):
            row[stat[0].replace('-', '')] = stat[2] % coll[i+1]  # e.g. 'llr': 33850.44
        collocation_output_data.append(row)

    return collocation_output_data, len(collocations)
