from . import cwb_input


def query(context_left_or_right='',
          context='1s',
          primary_lang='BIRM_ENG',
          show='+lemma +tag',
          print_structures='meta_case_name, meta_case_number, meta_date, meta_doc_cellar',
          A='[lemma="plea"%c]',
          start=1,
          length=500):
    """
    Performs a search command on CQP

    context_left_or_right = 'Left' or 'Right' or '' (empty) for both
    context = e.g. 5 words (see: https://cwb.sourceforge.io/files/CQP_Manual/2_3.html)
    primary_lang = e.g. BIRM_ENG, BIRM_DEU, etc. See all languages in REGISTRY path at top of this doc

    Example command:
    [word="plea"%c & lemma="ok" & ta="tag"]
    """

    cmd = [
        f'set {context_left_or_right}Context {context}; {primary_lang};\
        show {show}; set PrintStructures "{print_structures}"; A={A}; cat A {start} {length};'
    ]

    return cwb_input.execute(cmd).split('\n')
