from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin

from .forms import VotingForm, PollForm
from .models import Poll, Vote


class IndexView(LoginRequiredMixin, generic.TemplateView, FormMixin):
    template_name = 'polls/index.html'
    form_class = PollForm
    success_url = './'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        context['polls_list'] = Poll.objects.order_by('-pub_date')
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        user = self.request.user
        poll_title = form.cleaned_data.get("title")
        poll_description = form.cleaned_data.get("description")
        Poll.objects.create(user=user, poll_title=poll_title, poll_description=poll_description)
        return super().form_valid(form)


class DetailView(LoginRequiredMixin, generic.DetailView, FormMixin):
    model = Poll
    template_name = 'polls/detail.html'
    form_class = VotingForm
    success_url = './'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        context['voted'] = self.user_voted()
        return context

    def user_voted(self):
        poll = self.get_object()
        user = self.request.user
        votes = poll.vote_set.all()
        for vote in votes:
            if vote.user == user:
                return True
        return False

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        poll = self.get_object()
        user = self.request.user
        vote_value = form.cleaned_data.get("vote")
        Vote.objects.create(user=user, poll=poll, vote_value=vote_value)
        return super().form_valid(form)


class UpdateView(LoginRequiredMixin, generic.DetailView, FormMixin):
    model = Vote
    template_name = 'polls/update.html'
    form_class = VotingForm

    def get_success_url(self):
        vote = self.get_object()
        return '/polls/' + str(vote.poll.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        form = self.get_form()
        vote = self.get_object()
        if form.is_valid() and self.request.user == vote.user:
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        vote = self.get_object()
        vote_value = form.cleaned_data.get("vote")
        Vote.objects.filter(pk=vote.id).update(vote_value=vote_value)
        return super().form_valid(form)
