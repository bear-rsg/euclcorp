import re


def process(cwb_output):
    """
    Takes cwb_output (the string output generated by CWB) and processes it
    to turn into a proper data format suitable for consumption in a Django template
    """

    return [re.sub(r" \[.*", "", i).strip().split('\t') for i in cwb_output.strip().split(']')[:-1]]