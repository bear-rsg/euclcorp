from django.views.generic import TemplateView
from . import (cwb_input_search,
               cwb_input_frequency,
               cwb_input_collocations,
               cwb_input_ngrams,

               cwb_output_search,
               cwb_output_frequency,
               cwb_output_collocations,
               cwb_output_ngrams)


# These are all of the languages listed in the corpus registry dir:
# /rds/projects/m/mcaulifk-euclcorp-website/data/Corpus/Registry
PARALLEL_CORPORA_LIST = [
    {'id': 'birm_eng', 'name': 'English'},
    {'id': 'birm_fra', 'name': 'French'},
    {'id': 'birm_deu', 'name': 'German'},
    {'id': 'birm_bul', 'name': 'Bulgarian'},
    {'id': 'birm_ces', 'name': 'Czech'},
    {'id': 'birm_dan', 'name': 'Danish'},
    {'id': 'birm_ell', 'name': 'Greek'},
    {'id': 'birm_est', 'name': 'Estonian'},
    {'id': 'birm_fin', 'name': 'Finnish'},
    {'id': 'birm_hrv', 'name': 'Croatian'},
    {'id': 'birm_hun', 'name': 'Hungarian'},
    {'id': 'birm_ita', 'name': 'Italian'},
    {'id': 'birm_lav', 'name': 'Latvian'},
    {'id': 'birm_lit', 'name': 'Lithuanian'},
    {'id': 'birm_mlt', 'name': 'Maltese'},
    {'id': 'birm_nld', 'name': 'Dutch'},
    {'id': 'birm_pol', 'name': 'Polish'},
    {'id': 'birm_por', 'name': 'Portugese'},
    {'id': 'birm_ron', 'name': 'Romanian'},
    {'id': 'birm_slk', 'name': 'Slovak'},
    {'id': 'birm_slv', 'name': 'Slovenian'},
    {'id': 'birm_spa', 'name': 'Spanish'},
    {'id': 'birm_swe', 'name': 'Swedish'}
]

# These are all of the monolingual corpora included in the previous version of the website
MONOLINGUAL_CORPORA_LIST = [
    {'id': 'uk', 'name': 'UK National Court'},
    {'id': 'french', 'name': 'French National Court'},
    {'id': 'austrian', 'name': 'Austrian National Court'}
]


class InputMonolingualView(TemplateView):
    """
    Class-based view to show the input (monolingual) template
    """
    template_name = 'researchdata/input-monolingual.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['corpora_list'] = MONOLINGUAL_CORPORA_LIST
        return context


class InputParallelView(TemplateView):
    """
    Class-based view to show the input (parallel) template
    """
    template_name = 'researchdata/input-parallel.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['corpora_list'] = PARALLEL_CORPORA_LIST
        return context


class OutputView(TemplateView):
    """
    Class-based view to show the output template
    """
    template_name = 'researchdata/output.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        output_type = self.request.GET.get('outputtype', '')
        cwb_query = self.request.GET.get('cqpsearchquery', '')

        # Primary language
        # The language code to pass to CWB in upper, e.g. BIRM_ENG
        primary_language_code = self.request.GET.get('primarylanguage', '').upper()
        # The user-friendly name to display in client, e.g. English
        for language in PARALLEL_CORPORA_LIST:
            if language['id'] == primary_language_code.lower():
                primary_language_name = language['name']

        # Determine if input type was monolingual or parallel (parallel if languages are supplied)
        parallel_languages = self.request.GET.get('corpora-parallel-languages', '')
        parallel_languages_show = ''
        # Create str of languages ready for 'show' arg in cwb, e.g. " +birm_deu +birm_fra"
        if parallel_languages != '':
            for language in parallel_languages.split(','):
                parallel_languages_show += f" +{language}"

        context['output_type'] = output_type
        context['cwb_query'] = cwb_query
        context['primary_language'] = primary_language_name

        # Requires a query input (otherwise redirect to input page)
        if cwb_query != '':

            # Search
            if output_type == 'search':
                # 1. Get options from request
                options = {
                    'primary_language': primary_language_name,
                    'languages': parallel_languages_show,
                    'entriesperpage': self.request.GET.get('search-entriesperpage', ''),
                    'bigsizelimit': self.request.GET.get('search-bigsizelimit', '')
                }
                # 2. Query CWB
                cwb_output = cwb_input_search.query(
                    primary_lang=primary_language_code,
                    A=cwb_query,
                    length=500,
                    show=f"+lemma +tag{options['languages']}"
                )
                # 3. Return processed output
                context['query_output'] = cwb_output_search.process(cwb_query, cwb_output, options)

            # Frequency
            elif output_type == 'frequency':
                # 1. Get options from request
                options = {
                    'countby': self.request.GET.get('frequency-countby', '')
                }
                # 2. Query CWB
                cwb_output = cwb_input_frequency.query(
                    primary_lang=primary_language_code,
                    F=cwb_query,
                    countby=options['countby']
                )
                # 3. Return processed output
                context['query_output'] = cwb_output_frequency.process(cwb_output)

            # Collocations
            elif output_type == 'collocations':
                # 1. Get options from request
                options = {
                    'countby': self.request.GET.get('collocations-countby', 'word'),
                    'spanleft': int(self.request.GET.get('collocations-spanleft', '3')),
                    'spanright': int(self.request.GET.get('collocations-spanright', '3')),
                    'threshold': int(self.request.GET.get('collocations-frequencythreshold', '2')),

                    'llr': self.request.GET.get('collocations-llr', ''),
                    'mi': self.request.GET.get('collocations-mi', ''),
                    'tscore': self.request.GET.get('collocations-tscore', ''),
                    'zscore': self.request.GET.get('collocations-zscore', ''),
                    'dice': self.request.GET.get('collocations-dice', ''),
                    'mi3': self.request.GET.get('collocations-mi3', ''),
                    'frequency': self.request.GET.get('collocations-frequency', ''),

                    'ams': ['llr', 'mi', 't-score', 'z-score', 'dice', 'mi3', 'frequency'],

                    # 'sort': 1,

                    'primlang': primary_language_code,
                    'langs': ['birm_fra', 'birm_deu']
                }
                # 2. Query CWB
                cwb_output = cwb_input_collocations.query(
                    primary_lang=primary_language_code,
                    LeftContext=options['spanleft'],
                    RightContext=options['spanright'],
                    query=cwb_query
                )
                # 3. Return processed output
                context['query_output'], context['collocations_length'] = cwb_output_collocations.process(cwb_query, cwb_output, options)

            # N-grams
            elif output_type == 'ngrams':
                # 1. Get options from request
                options = {
                    'countby': self.request.GET.get('ngrams-countby', ''),
                    'size': int(self.request.GET.get('ngrams-size', 3)),
                    'frequencythreshold': int(self.request.GET.get('ngrams-frequencythreshold', 3))
                }
                # 2. Query CWB
                cwb_output = cwb_input_ngrams.query(
                    primary_lang=primary_language_code,
                    Context=options['size'],
                    query=cwb_query
                )
                # 3. Return processed output
                context['query_output'] = cwb_output_ngrams.process(cwb_query, cwb_output, options)

        return context
