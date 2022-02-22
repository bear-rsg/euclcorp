from subprocess import check_output


def execute(cmd):
    """
    Executes a command on CQP

    cmd = list of CWB command args (excludes the default args shown below)

    This script is designed to be used by other cwb_input_XXX.py files in this dir, e.g. search, frequency, ngrams, collocations
    """

    # Default command args, plus cmd args passed to function
    cmd = [
        "/rds/projects/m/mcaulifk-euclcorp-website/cwb/bin/cqpcl",
        "-r",
        "/rds/projects/m/mcaulifk-euclcorp-website/data/Corpus/Registry"
    ] + cmd

    return check_output(cmd, universal_newlines=True)
