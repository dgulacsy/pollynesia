from django.views import generic

class LandingPage(generic.base.TemplateView):
    template_name = 'pollynesia_site/landing_page.html'