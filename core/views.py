from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView, FormView
from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import PermissionDenied
from .models import *
from .forms import *

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
    paginate_by = 5

class DestinationDetailView(DetailView):
    model = Destination
    template_name = "destination/destination_detail.html"

    def get_context_data(self, **kwargs):
        context = super(DestinationDetailView, self).get_context_data(**kwargs)
        destination = Destination.objects.get(id=self.kwargs['pk'])
        recommendations = Recommendation.objects.filter(destination=destination)
        context['recommendations'] = recommendations
        user_recommendations = Recommendation.objects.filter(destination=destination, user=self.request.user)
        context['user_recommendations'] = user_recommendations
        user_votes = Recommendation.objects.filter(vote__user=self.request.user)
        context['user_votes'] = user_votes
        return context

class DestinationUpdateView(UpdateView):
    model = Destination
    template_name = 'destination/destination_form.html'
    fields = ['destination', 'point_of_interest']

    def get_object(self, *args, **kwargs):
        object = super(DestinationUpdateView, self).get_object(*args, **kwargs)
        if object.user != self.request.user:
           raise PermissionDenied()
        return object

class DestinationDeleteView(DeleteView):
    model = Destination
    template_name = 'destination/destination_confirm_delete.html'
    success_url = reverse_lazy('destination_list')

    def get_object(self, *args, **kwargs):
        object = super(DestinationDeleteView, self).get_object(*args, **kwargs)
        if object.user != self.request.user:
           raise PermissionDenied()
        return object

class RecommendationCreateView(CreateView):
    model = Recommendation
    template_name = "recommendation/recommendation_form.html"
    fields = ['recommendation']

    def get_success_url(self):
        return self.object.destination.get_absolute_url()

    def form_valid(self, form):
        destination = Destination.objects.get(id=self.kwargs['pk'])
        if Recommendation.objects.filter(destination=destination, user=self.request.user).exists():
          raise PermissionDenied()
        form.instance.user = self.request.user
        form.instance.destination = Destination.objects.get(id=self.kwargs['pk'])
        return super(RecommendationCreateView, self).form_valid(form)

class RecommendationUpdateView(UpdateView):
    model = Recommendation
    pk_url_kwarg = 'recommendation_pk'
    template_name = 'recommendation/recommendation_form.html'
    fields = ['recommendation']

    def get_success_url(self):
        return self.object.destination.get_absolute_url()

    def get_object(self, *args, **kwargs):
      object = super(RecommendationUpdateView, self).get_object(*args, **kwargs)
      if object.user != self.request.user:
         raise PermissionDenied()
      return object

class RecommendationDeleteView(DeleteView):
    model = Recommendation
    pk_url_kwarg = 'recommendation_pk'
    template_name = 'recommendation/recommendation_confirm_delete.html'

    def get_success_url(self):
        return self.object.destination.get_absolute_url()

    def get_object(self, *args, **kwargs):
      object = super(RecommendationDeleteView, self).get_object(*args, **kwargs)
      if object.user != self.request.user:
         raise PermissionDenied()
      return object

class VoteFormView(FormView):
    form_class = VoteForm

    def form_valid(self, form):
      user = self.request.user
      recommendation = Recommendation.objects.get(pk=form.data["recommendation"])
      prev_votes = Vote.objects.filter(user=user, recommendation=recommendation)
      has_voted = (prev_votes.count()>0)
      if not has_voted:
        Vote.objects.create(user=user, recommendation=recommendation)
      else:
         prev_votes[0].delete()
      return redirect(reverse('destination_detail', args=[form.data["destination"]]))

class UserDetailView(DetailView):
  model = User
  slug_field = 'username'
  template_name = 'user/user_detail.html'
  context_object_name = 'user_in_view'

  def get_context_data(self, **kwargs):
      context = super(UserDetailView, self).get_context_data(**kwargs)
      user_in_view = User.objects.get(username=self.kwargs['slug'])
      destinations = Destination.objects.filter(user=user_in_view)
      context['destinations'] = destinations
      recommendations = Recommendation.objects.filter(user=user_in_view)
      context['recommendations'] = recommendations
      return context

class UserUpdateView(UpdateView):
  model = User
  slug_field = "username"
  template_name = "user/user_form.html"
  fields = ['email', 'first_name', 'last_name']

  def get_success_url(self):
      return reverse('user_detail', args=[self.request.user.username])

  def get_object(self, *args, **kwargs):
      object = super(UserUpdateView, self).get_object(*args, **kwargs)
      if object != self.request.user:
        raise PermissionDenied()
      return object

class UserDeleteView(DeleteView):
  model = User
  slug_field = "username"
  template_name = 'user/user_confirm_delete.html'

  def get_success_url(self):
      return reverse_lazy('logout')

  def get_object(self, *args, **kwargs):
      object = super(UserDeleteView, self).get_object(*args, **kwargs)
      if object != self.request.user:
        raise PermissionDenied()
      return object

  def delete(self, request, *args, **kwargs):
      user = super(UserDeleteView, self).get_object(*args)
      user.is_active = False
      user.save()
      return redirect(self.get_success_url())

class SearchDestinationListView(DestinationListView):
  def get_queryset(self):
      incoming_query_string = self.request.GET.get('query','')
      return Destination.objects.filter(destination__icontains=incoming_query_string)