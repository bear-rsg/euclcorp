from django.views.generic import TemplateView
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
        query_input = self.request.GET.get('cqpsearch', '')
        context['query_input'] = query_input

        if query_input != '':
            context['query_output'] = cwb_exec.query(
                A=query_input,
                length=50
            )
        return context


class ParallelCorpusView(TemplateView):
    """
    Class-based view to show the Parallel Corpus template
    """
    template_name = 'researchdata/parallel-corpus.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query_input = self.request.GET.get('cqpsearch', '')
        context['query_input'] = query_input
        context['query_output'] = cwb_exec.query(A=query_input)
        return context
