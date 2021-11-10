from django.views.generic import TemplateView


class TestView(TemplateView):
    """
    Class-based view to show the test template
    """
    template_name = 'researchdata/test.html'
