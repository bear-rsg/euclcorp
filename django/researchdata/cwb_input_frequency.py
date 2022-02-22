from . import cwb_input


def query(primary_lang='BIRM_ENG', F='[word="plea"%c]', countby='word'):
    """
    Performs a frequency command on CQP

    Example command:
    BIRM_ENG; F=[word="plea"%c]; count F by word;
    """

    cmd = [
        f'{primary_lang}; F={F}; count F by {countby};'
    ]

    return cwb_input.execute(cmd)
