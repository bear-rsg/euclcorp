from django.views.generic import TemplateView
from django.urls import reverse_lazy
from . import cwb_exec


class MonolingualCorporaInputView(TemplateView):
    """
    Class-based view to show the Monolingual Corpora input template
    """
    template_name = 'researchdata/monolingual-corpora-input.html'


class MonolingualCorporaOutputView(TemplateView):
    """
    Class-based view to show the Monolingual Corpora output (Search) template
    """
    template_name = 'researchdata/monolingual-corpora-output.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        output_type = self.request.GET.get('outputtype', 'search')
        query_input = self.request.GET.get('cqpsearchquery', '')

        context['output_type'] = output_type
        context['query_input'] = query_input

        # Requires a query input (otherwise redirect to input page)
        if query_input != '':
            # Search
            if output_type == 'search':
                context['query_output'] = cwb_exec.query(
                    A=query_input,
                    length=50
                )
            # Frequency
            if output_type == 'frequency':
                pass
            # Collocations
            if output_type == 'collocations':
                pass
            # N-grams
            if output_type == 'ngrams':
                pass

            return context
        else:
            return reverse_lazy('researchdata:monolingual-input')


class ParallelCorpusView(TemplateView):
    """
    Class-based view to show the Parallel Corpus template
    """
    template_name = 'researchdata/parallel-corpus.html'
