from subprocess import check_output

#/rds/projects/m/mcaulifk-euclcorp-website/cwb/bin/cqpcl -r /rds/projects/m/mcaulifk-euclcorp-website/data/Corpus/Registry 'set Context 1s; BIRM_ENG; show +lemma +tag +birm_deu +birm_fra; set PrintStructures "meta_case_name, meta_case_number, meta_date, meta_doc_cellar"; A=[word="Court"%c]; cat A 1 3;' 

CQPCL = "/rds/projects/m/mcaulifk-euclcorp-website/cwb/bin/cqpcl"
REGISTRY = "/rds/projects/m/mcaulifk-euclcorp-website/data/Corpus/Registry"
ENG = "BIRM_ENG"


def query():
    """
    ...
    """

    cmd = [CQPCL, "-r", REGISTRY, 'set Context 1s; BIRM_ENG; show +lemma +tag +birm_deu +birm_fra; set PrintStructures "meta_case_name, meta_case_number, meta_date, meta_doc_cellar"; A=[word="Court"%c]; cat A 1 2;']

    out = check_output(cmd, universal_newlines=True)
    print(out)


if __name__ == "__main__":
    query()