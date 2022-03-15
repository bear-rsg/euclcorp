from subprocess import check_output


def execute(cwb_cmd_args):
    """
    Executes a command on CQP

    cwb_cmd_args = list of CWB command args (excludes the default args shown below)

    This function is designed to be used by other cwb_input_XXX.py files in this dir
    e.g. search, frequency, ngrams, collocations
    """

    # Default command args, plus cmd args passed to function
    cwb_cmd = [
        "/rds/projects/m/mcaulifk-euclcorp-website/cwb/bin/cqpcl",
        "-r",
        "/rds/projects/m/mcaulifk-euclcorp-website/data/Corpus/Registry"
    ] + cwb_cmd_args

    return check_output(cwb_cmd, universal_newlines=True)
