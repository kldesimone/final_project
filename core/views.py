from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, ListView
from django.core.urlresolvers import reverse_lazy
from .models import *

# Create your views here.
class Home(TemplateView):
    template_name = "home.html"

class DestinationCreateView(CreateView):
    model = Destination
    template_name = "destination/destination_form.html"
    fields = ['destination', 'point_of_interest']
    success_url = reverse_lazy('destination_list')

    def form_valid(self, form):
      form.instance.user = self.request.user
      return super(DestinationCreateView, self).form_valid(form)

class DestinationListView(ListView):
    model = Destination
    template_name = "destination/destination_list.html"