from django.views.generic import TemplateView
from . import cwb_exec


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
        query_input = self.request.GET.get('cqpsearchquery', '')

        context['output_type'] = output_type
        context['query_input'] = query_input

        # Requires a query input (otherwise redirect to input page)
        if query_input != '':
            # Search
            if output_type == 'search':
                # Options
                option_entriesperpage = self.request.GET.get('search-entriesperpage', '')
                option_displaymode = self.request.GET.get('search-displaymode', '')
                option_bigsizelimit = self.request.GET.get('search-bigsizelimit', '')
                option_showmetadata = self.request.GET.get('search-showmetadata', '')
                # Query
                context['query_output'] = cwb_exec.query(
                    A=query_input,
                    length=50
                )
            # Frequency
            if output_type == 'frequency':
                # Options
                option_countby = self.request.GET.get('frequency-countby', '')
                # Query
                context['query_output'] = cwb_exec.frequency(
                    F=query_input,
                    countby=option_countby
                )
            # Collocations
            if output_type == 'collocations':
                # Options
                option_countby = self.request.GET.get('collocations-countby', '')
                option_spanleft = self.request.GET.get('collocations-spanleft', '')
                option_spanright = self.request.GET.get('collocations-spanright', '')
                option_frequencythreshold = self.request.GET.get('collocations-frequencythreshold', '')
                option_llr = self.request.GET.get('collocations-llr', '')
                option_mi = self.request.GET.get('collocations-mi', '')
                option_tscore = self.request.GET.get('collocations-tscore', '')
                option_zscore = self.request.GET.get('collocations-zscore', '')
                option_dice = self.request.GET.get('collocations-dice', '')
                option_mi3 = self.request.GET.get('collocations-mi3', '')
                option_frequency = self.request.GET.get('collocations-frequency', '')
                # Query
                context['query_output'] = cwb_exec.collocations(
                    LeftContext=option_spanleft,
                    RightContext=option_spanright,
                    query=query_input
                )
            # N-grams
            if output_type == 'ngrams':
                # Options
                option_ = self.request.GET.get('ngrams-', '')
                # 

        return context


class ParallelCorpusView(TemplateView):
    """
    Class-based view to show the Parallel Corpus template
    """
    template_name = 'researchdata/parallel-corpus.html'
