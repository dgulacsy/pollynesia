from .utils import download
from .models import Poll, Choice, Vote
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.forms import inlineformset_factory, ModelForm
import logging

logger = logging.getLogger(__name__)


class IndexView(generic.ListView):
    model = Poll
    template_name = 'polls/index.html'
    context_object_name = 'latest_poll_list'
    paginate_by = 10

    def get_queryset(self):
        """Return the last 5 published polls of logged in user"""
        return Poll.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class UserIndexView(generic.ListView):
    model = Poll
    template_name = 'polls/user_polls.html'
    context_object_name = 'polls'
    paginate_by = 10

    def get_queryset(self):
        """Return the published polls of logged in user"""
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Poll.objects.filter(user=user).filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')


class DetailView(generic.DetailView):
    model = Poll
    template_name = 'polls/detail.html'

    def get_queryset(self):
        return Poll.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Poll
    template_name = 'polls/results.html'


class PollForm(ModelForm):
    class Meta:
        model = Poll
        fields = ['title', 'description', 'location', 'open_from', 'close_at']


class CreateView(LoginRequiredMixin, generic.CreateView):
    model = Poll
    template_name = 'polls/poll_form.html'
    form_class = PollForm
    success_url = "/polls"

    def __init__(self):
        self.ChoiceFormset = inlineformset_factory(
            Poll, Choice, fields=('choice_text',), extra=3)
        super().__init__()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PollForm()
        context['formset'] = self.ChoiceFormset()
        return context

    def post(self, request, *args, **kwargs):
        poll_form = PollForm(data=request.POST)
        self.object = poll_form
        choice_formset = self.ChoiceFormset(
            request.POST, instance=poll_form.instance)
        print(choice_formset.is_valid(), poll_form.is_valid())
        if choice_formset.is_valid() and poll_form.is_valid():
            return self.form_valid(choice_formset, poll_form)
        else:
            messages.warning(request, 'Invalid form! Please try again!')
            return self.form_invalid(choice_formset)

    def form_valid(self, formset, poll_form):
        poll_form.instance.user = self.request.user
        poll_form.save()
        choice_forms = formset.save(commit=False)
        print(choice_forms)
        for choice_form in choice_forms:
            choice_form.save()
        return HttpResponseRedirect(self.get_success_url())


class UpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Poll
    template_name = 'polls/poll_form.html'
    form_class = PollForm

    def __init__(self):
        self.ChoiceFormset = inlineformset_factory(
            Poll, Choice, fields=('choice_text',), extra=0)
        super().__init__()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PollForm(instance=self.object)
        context['formset'] = self.ChoiceFormset(instance=self.object)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        print('running post')
        poll_form = PollForm(data=request.POST, instance=self.object)
        choice_formset = self.ChoiceFormset(
            request.POST, instance=self.object)
        if choice_formset.is_valid() and poll_form.is_valid():
            return self.form_valid(choice_formset, poll_form)
        else:
            HttpResponseRedirect(
                reverse('polls:update', args=(self.object.id,)))

    def form_valid(self, formset, poll_form):
        print('form_valid')
        poll_form.instance.user = self.request.user
        self.object = poll_form.save()
        formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def test_func(self):
        poll = self.get_object()
        return self.request.user == poll.user


class DeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Poll
    success_url = '/polls'

    def test_func(self):
        poll = self.get_object()
        return self.request.user == poll.user


def vote(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    logger.info('initiating vote for %s', poll)
    try:
        voter_name = request.POST['voter_name']
        selected_choice = poll.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        logger.debug('No choice selected on form')
        messages.warning(request, 'Please select a choice!')
        return HttpResponseRedirect(reverse('polls:detail', args=(poll.id,)))
    else:
        vote = Vote(choice=selected_choice, voter_name=voter_name)
        vote.save()
        logger.info('added vote for %s', poll)
        return HttpResponseRedirect(reverse('polls:results', args=(poll.id,)))


@login_required
def download_votes(request, poll_id, format='csv'):
    poll = get_object_or_404(Poll, pk=poll_id)
    votes_queryset = Vote.objects.all().filter(choice__poll=poll)
    response = download(votes_queryset, format)
    return response
