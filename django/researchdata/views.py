from django.views.generic import TemplateView
from . import cwb_exec


class MonolingualCorporaView(TemplateView):
    """
    Class-based view to show the Monolingual Corpora template
    """
    template_name = 'researchdata/monolingual-corpora.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query_input = self.request.GET.get('query', '')
        context['query_input'] = query_input
        context['query_output'] = cwb_exec.query(context=query_input).split('\n')[0]
        return context


class ParallelCorpusView(TemplateView):
    """
    Class-based view to show the Parallel Corpus template
    """
    template_name = 'researchdata/parallel-corpus.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query_input = self.request.GET.get('query', '')
        context['query_input'] = query_input
        context['query_output'] = cwb_exec.query(context=query_input).split('\n')[0]
        return context
