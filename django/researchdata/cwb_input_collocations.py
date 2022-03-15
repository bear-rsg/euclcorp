from . import cwb_input


def query(primary_lang='BIRM_ENG', LeftContext=3, RightContext=3, query='[word="plea"%c]'):
    """
    Performs a collocations command on CQP

    Example command:
    BIRM_ENG; set LeftContext 5 words; set RightContext 2 words; show -cpos; show +lemma; [word="the"%c];
    """

    cwb_cmd_args = [
        f'{primary_lang}; set LeftContext {LeftContext} words;\
        set RightContext {RightContext} words; show -cpos; show +lemma; {query};'
    ]

    return cwb_input.execute(cwb_cmd_args)
