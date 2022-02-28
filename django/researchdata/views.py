from django.views.generic import TemplateView
from . import (cwb_input_search,
               cwb_input_frequency,
               cwb_input_collocations,
               cwb_input_ngrams,

               cwb_output_search,
               cwb_output_frequency,
               # cwb_output_collocations,
               cwb_output_ngrams)


class InputMonolingualView(TemplateView):
    """
    Class-based view to show the input (monolingual) template
    """
    template_name = 'researchdata/input-monolingual.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['corpora_list'] = [
            {
                'id': 'uk',
                'name': 'UK National Court'
            },
            {
                'id': 'french',
                'name': 'French National Court'
            },
            {
                'id': 'austrian',
                'name': 'Austrian National Court'
            }
        ]
        return context


class InputParallelView(TemplateView):
    """
    Class-based view to show the input (parallel) template
    """
    template_name = 'researchdata/input-parallel.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['corpora_list'] = [
            {
                'id': 'birm_eng',
                'name': 'English'
            },
            {
                'id': 'birm_fra',
                'name': 'French'
            },
            {
                'id': 'birm_deu',
                'name': 'German'
            }
        ]
        return context


class MonolingualCorporaOutputView(TemplateView):
    """
    Class-based view to show the Monolingual Corpora output template
    """
    template_name = 'researchdata/monolingual-corpora-output.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        output_type = self.request.GET.get('outputtype', '')
        cwb_query = self.request.GET.get('cqpsearchquery', '')

        context['output_type'] = output_type
        context['cwb_query'] = cwb_query

        # Requires a query input (otherwise redirect to input page)
        if cwb_query != '':

            # Search
            if output_type == 'search':
                # Options

                # 1. Get options from request
                options = {
                    'entriesperpage': self.request.GET.get('search-entriesperpage', ''),
                    'displaymode': self.request.GET.get('search-displaymode', ''),
                    'bigsizelimit': self.request.GET.get('search-bigsizelimit', ''),
                    'showmetadata': self.request.GET.get('search-showmetadata', '')
                }

                # 2. Query CWB
                cwb_output = cwb_input_search.query(
                    A=cwb_query,
                    length=500
                )

                # 3. Return processed output
                context['query_output'] = cwb_output_search.process(cwb_query, cwb_output, options)

            # Frequency
            if output_type == 'frequency':

                # 1. Get options from request
                options = {
                    'countby': self.request.GET.get('frequency-countby', '')
                }

                # 2. Query CWB
                cwb_output = cwb_input_frequency.query(
                    F=cwb_query,
                    countby=options['countby']
                )

                # 3. Return processed output
                context['query_output'] = cwb_output_frequency.process(cwb_output)

            # Collocations
            if output_type == 'collocations':

                # 1. Get options from request
                options = {
                    'countby': self.request.GET.get('collocations-countby', ''),
                    'spanleft': self.request.GET.get('collocations-spanleft', ''),
                    'spanright': self.request.GET.get('collocations-spanright', ''),
                    'frequencythreshold': self.request.GET.get('collocations-frequencythreshold', ''),
                    'llr': self.request.GET.get('collocations-llr', ''),
                    'mi': self.request.GET.get('collocations-mi', ''),
                    'tscore': self.request.GET.get('collocations-tscore', ''),
                    'zscore': self.request.GET.get('collocations-zscore', ''),
                    'dice': self.request.GET.get('collocations-dice', ''),
                    'mi3': self.request.GET.get('collocations-mi3', ''),
                    'frequency': self.request.GET.get('collocations-frequency', ''),
                }

                # 2. Query CWB
                cwb_output = cwb_input_collocations.query(
                    LeftContext=options['spanleft'],
                    RightContext=options['spanright'],
                    query=cwb_query
                )

                # 3. Return processed output
                context['query_output'] = True

            # N-grams
            if output_type == 'ngrams':

                # 1. Get options from request
                options = {
                    'countby': self.request.GET.get('ngrams-countby', ''),
                    'size': int(self.request.GET.get('ngrams-size', 3)),
                    'frequencythreshold': int(self.request.GET.get('ngrams-frequencythreshold', 3))
                }

                # 2. Query CWB
                cwb_output = cwb_input_ngrams.query(
                    Context=options['size'],
                    query=cwb_query
                )

                # 3. Return processed output
                context['query_output'] = cwb_output_ngrams.process(cwb_query, cwb_output, options)

        return context

