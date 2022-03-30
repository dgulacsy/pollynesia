from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views import generic
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.forms import inlineformset_factory, ModelForm

from .models import Poll, Choice, Vote


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


ChoiceFormset = inlineformset_factory(
    Poll, Choice, fields=('choice_text',), extra=2)


class CreateView(LoginRequiredMixin, generic.CreateView):
    model = Poll
    template_name = 'polls/poll_form.html'
    form_class = PollForm
    success_url = "/polls"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PollForm()
        context['formset'] = ChoiceFormset()
        return context

    def post(self, request, *args, **kwargs):
        poll_form = PollForm(data=request.POST)
        choice_formset = ChoiceFormset(
            request.POST, instance=poll_form.instance)
        if choice_formset.is_valid() and poll_form.is_valid():
            return self.form_valid(choice_formset, poll_form)

    def form_valid(self, formset, poll_form):
        self.object = poll_form
        poll_form.instance.user = self.request.user
        poll_form.save()
        choice_forms = formset.save(commit=False)
        print(choice_forms)
        for choice_form in choice_forms:
            choice_form.save()
        return HttpResponseRedirect(self.get_success_url())


class UpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Poll
    fields = ['title', 'description', 'location', 'open_from', 'close_at']
    template_name = 'polls/poll_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

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
    retry = False
    context = {
        'poll': poll,
    }
    try:
        voter_name = request.POST['voter_name']
        if not voter_name:
            retry = True
            context['no_name_error_message'] = "Please add your name"
        selected_choice = poll.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        retry = True
        context['selection_error_message'] = "You didn't select a choice"
    if retry:
        print(context)
        return render(request, 'polls/detail.html', context=context)
    else:
        vote = Vote(choice=selected_choice, voter_name=voter_name)
        vote.save()
        return HttpResponseRedirect(reverse('polls:results', args=(poll.id,)))
