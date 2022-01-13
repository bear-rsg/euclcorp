from django.views.generic import TemplateView
from . import cwb_exec


class TestView(TemplateView):
    """
    Class-based view to show the test template
    """
    template_name = 'researchdata/test.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query_input = self.request.GET.get('query', 'x')
        context['query_input'] = query_input
        context['query_output'] = cwb_exec.query(context=query_input).split('\n')[0]
        return context

