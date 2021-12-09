from subprocess import check_output

#/rds/projects/m/mcaulifk-euclcorp-website/cwb/bin/cqpcl -r /rds/projects/m/mcaulifk-euclcorp-website/data/Corpus/Registry 'set Context 1s; BIRM_ENG; show +lemma +tag +birm_deu +birm_fra; set PrintStructures "meta_case_name, meta_case_number, meta_date, meta_doc_cellar"; A=[word="Court"%c]; cat A 1 3;' 

CQPCL = "/rds/projects/m/mcaulifk-euclcorp-website/cwb/bin/cqpcl"
REGISTRY = "/rds/projects/m/mcaulifk-euclcorp-website/data/Corpus/Registry"


def query(context_left_or_right='',
          context='3 words',
          primary_lang='BIRM_ENG',
          show='+lemma +tag +birm_deu +birm_fra',
          print_structures='meta_case_name, meta_case_number, meta_date, meta_doc_cellar',
          A='[lemma="plea"%c]',
          start=1,
          length=5):
    """
    Performs a query on CQP. 
    
    context_left_or_right = 'Left' or 'Right' or '' (empty) for both
    context = e.g. 5 words (see: https://cwb.sourceforge.io/files/CQP_Manual/2_3.html)
    """

    cmd = [CQPCL, "-r", REGISTRY, f'set {context_left_or_right}Context {context}; {primary_lang}; show {show}; set PrintStructures "{print_structures}"; A={A}; cat A {start} {length};']


    out = check_output(cmd, universal_newlines=True)
    out_list = out.split('\n')
    for o in out_list:
        print(o, '\n\n\n')


if __name__ == "__main__":
    query()