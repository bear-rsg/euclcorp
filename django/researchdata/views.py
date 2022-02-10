from django.views.generic import TemplateView
from . import (cwb_exec, cwb_process_search, cwb_process_frequency, cwb_process_collocations, cwb_process_ngrams)
import re


class MonolingualCorporaInputView(TemplateView):
    """
    Class-based view to show the Monolingual Corpora input template
    """
    template_name = 'researchdata/monolingual-corpora-input.html'


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
                # option_entriesperpage = self.request.GET.get('search-entriesperpage', '')
                # option_displaymode = self.request.GET.get('search-displaymode', '')
                # option_bigsizelimit = self.request.GET.get('search-bigsizelimit', '')
                # option_showmetadata = self.request.GET.get('search-showmetadata', '')
                # Query
                context['query_output'] = cwb_exec.query(
                    A=cwb_query,
                    length=50
                )

            # Frequency
            if output_type == 'frequency':
                
                # 1. Get options from request
                options = {
                    'countby': self.request.GET.get('frequency-countby', '')
                }

                # 2. Query CWB
                cwb_output = cwb_exec.frequency(
                    F=cwb_query,
                    countby=options['countby']
                )

                # 3. Return processed output
                context['query_output'] = cwb_process_frequency.process(cwb_output)

            # Collocations
            if output_type == 'collocations':
                # Options
                # option_countby = self.request.GET.get('collocations-countby', '')
                option_spanleft = self.request.GET.get('collocations-spanleft', '')
                option_spanright = self.request.GET.get('collocations-spanright', '')
                # option_frequencythreshold = self.request.GET.get('collocations-frequencythreshold', '')
                # option_llr = self.request.GET.get('collocations-llr', '')
                # option_mi = self.request.GET.get('collocations-mi', '')
                # option_tscore = self.request.GET.get('collocations-tscore', '')
                # option_zscore = self.request.GET.get('collocations-zscore', '')
                # option_dice = self.request.GET.get('collocations-dice', '')
                # option_mi3 = self.request.GET.get('collocations-mi3', '')
                # option_frequency = self.request.GET.get('collocations-frequency', '')
                # Query
                context['query_output'] = cwb_exec.collocations(
                    LeftContext=option_spanleft,
                    RightContext=option_spanright,
                    query=cwb_query
                )

            # N-grams
            if output_type == 'ngrams':
                
                # 1. Get options from request
                options = {
                    'countby': self.request.GET.get('ngrams-countby', ''),
                    'size': int(self.request.GET.get('ngrams-size', 3)),
                    'frequencythreshold': int(self.request.GET.get('ngrams-frequencythreshold', 3))
                }

                # 2. Query CWB
                cwb_output = cwb_exec.ngrams(
                    Context=options['size'],
                    query=cwb_query
                )

                # 3. Return processed output
                context['query_output'] = cwb_process_ngrams.process(cwb_query, cwb_output, options)

        return context


class ParallelCorpusView(TemplateView):
    """
    Class-based view to show the Parallel Corpus template
    """
    template_name = 'researchdata/parallel-corpus.html'
