from . import cwb_input


def query(primary_lang='BIRM_ENG', Context=4, query='[word="plea"%c]'):
    """
    Performs a collocations command on CQP

    Example command:
    # BIRM_ENG; set Context 4 words; show -cpos; show +lemma; [word="plea"%c];
    """

    cwb_cmd_args = [
        f'{primary_lang}; set Context {Context} words; show -cpos; show +lemma; {query};'
    ]

    return cwb_input.execute(cwb_cmd_args)
