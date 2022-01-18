from django.views.generic import TemplateView


class WelcomeTemplateView(TemplateView):
    """
    Class-based view to show the welcome template
    """
    template_name = 'general/welcome.html'


class AboutTemplateView(TemplateView):
    """
    Class-based view to show the about template
    """
    template_name = 'general/about.html'


class ContactTemplateView(TemplateView):
    """
    Class-based view to show the contact template
    """
    template_name = 'general/contact.html'


class CookiesTemplateView(TemplateView):
    """
    Class-based view to show the cookies template
    """
    template_name = 'general/cookies.html'
