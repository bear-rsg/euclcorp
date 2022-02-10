import re


def process(cwb_query, cwb_output, options):
    """
    Takes cwb_output (the string output generated by CWB) and processes it 
    to turn into a proper data format suitable for consumption in a Django template
    """

    ngrams = {}
    node = u''
    cs = True if '%c' in cwb_query.split(']')[0] else false  # Case sensitity, from first/primary query
    # Build ngrams
    for line in cwb_output.splitlines():
        words = [el.rsplit('/', 1)[options['countby'] == 'lemma' and 1 or 0] for el in line.strip().split()]
        if not cs:
            words = [w.lower () for w in words]
        words = tuple (words)
        for ng in [words[i:i+options['size']] for i in range (len(words) - options['size'] + 1)]:
            if ng in ngrams:
                ngrams[ng] += 1
            else:
                ngrams[ng] = 1
    # Sort ngrams
    ngrams = sorted ([[ngram, freq] for ngram, freq in ngrams.items () if freq > options['frequencythreshold']], key = lambda x: x[1], reverse = True)
    # Process ngram words lists
    for ngram in ngrams:
        ngram[0] = ' '.join(ngram[0])  # Convert list of words to string
        ngram[0] = re.sub("<(\S*)|(\S*)>", r"<strong>\1\2</strong>", ngram[0])  # Wrap query word in strong tags
    return ngrams
