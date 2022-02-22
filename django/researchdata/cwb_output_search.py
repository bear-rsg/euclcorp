import re


def cwb_output_language_human_readable(raw_text):
    """
    This takes in the raw text from the CWB output of text and makes it human readable.
    It's used in the below 'process()' function by each language that's being shown on the page (i.e. the primary language and all secondary languages)
    It takes the first word before each forward slash and ignores the rest

    Example - raw_text input:
    By/IN/by its/PPZ/its first/JJ/first <plea/NN/plea> ,/,/, the/DT/the French/JJ/French Government/NN/government claims/VVZ/claim

    Example - human readable output:
    By its first plea, the French Government claims 
    """

    words = []
    for l in raw_text.split(' '):
        try:
            words.append(l.split('/')[0])
        except IndexError:
            pass  # Index errors are expected sometimes
    words_as_string = " ".join(words)

    # Remove unwanted spaces around certain chars
    # E.g. don't want a space before the comma in  "this is , an example"
    unwanted_whitespace_items = [' ,', ' .', '( ', '’ ', ' )', ' ?', ' !', "' ", '" ', ' "']
    for i in unwanted_whitespace_items:
        words_as_string = words_as_string.replace(i, i.strip())

    return words_as_string


def kwic_html(primary_language_content):
    """
    This takes the full text of the primary language and returns "Left", "Match", and "Right" HTML divs:
    Match = the searched for word from the CWB query
    Left & Right = up to 10 words either side of the matched word in the text
    """

    words = primary_language_content.strip().split(' ')
    match_index = 0
    # Find index of match (first instance of a word starting with < angled bracket)
    for i, word in enumerate(words):
        # print(word)
        try:
            if word[0] == '<':
                match_index = i
                break
        except IndexError:
            pass  # expected
    
    # Determine the left and right context indices, to prevent the index from being invalid
    # e.g. left context index below 0 or right context index greater than length of the words list
    max_context = 10
    left_context_index = 0 if match_index < max_context else match_index - max_context
    right_context_index = len(words) if match_index + max_context > len(words) else match_index + max_context

    return {
        'left_context': ' '.join(words[left_context_index:match_index]),
        'match': words[match_index][1:],
        'right_context':  ' '.join(words[match_index + 1:right_context_index])
    }


def process(cwb_query, cwb_output, options):
    """
    Takes cwb_output (the string output generated by CWB) and processes it 
    to turn into a proper data format suitable for consumption in a Django template
    """

    all_results = []

    for line in cwb_output:
        
        if line.strip().split(':')[0].isnumeric():
            # Each result starts with its metadata
            # So append previous result object to result list (if exists - i.e. is not the first result)
            # and start a new blank result object
            try:
                result['languages'] = languages
                all_results.append(result)
            except UnboundLocalError:
                pass  # this will happen for the first loop, when result hasn't yet been declared
            result = {}
            languages = []

            # Meta
            meta_obj = {}
            # Split each meta statement
            meta = line.strip().split(':')[1].strip()[:-1].split('><')
            # Add the meta fields in below list to the meta object
            for i, m in enumerate(['case_name', 'case_number', 'case_date', 'doc_cellar']):
                # Some results don't have all meta fields, so break loop to prevent index error
                if i == len(meta):
                    break
                meta_obj[m] = meta[i].split(' ', 1)[1]
            # Add to the current result
            result['meta'] = meta_obj

            # Primary Language
            primary_language_content = cwb_output_language_human_readable(line.split('>:')[-1])
            languages.append({
                'language_code': 'english',
                'content': primary_language_content,
                'kwic': kwic_html(primary_language_content)
            })


        # Secondary Languages
        if line.strip().startswith('-->'):
            lang = line.strip().split(' ', 1)
            
            

            # Add the finished sentence
            languages.append({
                'language_code': lang[0][3:-1],  # e.g. 'birm_deu' in '-->birm_deu:'
                # 'content': "".join([word for word in [l.split('/')[0] for l in lang[1:]]])
                'content': cwb_output_language_human_readable(lang[1])
            })

    # return cwb_output
    return all_results


