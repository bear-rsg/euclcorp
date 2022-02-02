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
                # Query
                context['query_output'] = cwb_exec.query(
                    A=query_input,
                    length=50
                )
            # Frequency
            if output_type == 'frequency':
                pass  # will be filled out in next PR
            # Collocations
            if output_type == 'collocations':
                pass  # will be filled out in next PR
            # N-grams
            if output_type == 'ngrams':
                pass  # will be filled out in next PR

        return context


class ParallelCorpusView(TemplateView):
    """
    Class-based view to show the Parallel Corpus template
    """
    template_name = 'researchdata/parallel-corpus.html'
