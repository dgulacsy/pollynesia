import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Poll

class pollModelTest(TestCase):
    def test_was_published_recently_with_future_pub_date(self):
        """
        Test whether was_published_recently() returns False for polls whose pub_date is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_poll = Poll(pub_date=time)
        self.assertIs(future_poll.was_published_recently(),False)

    def test_was_published_recently_with_old_pub_date(self):
        """
        Test whether was_published_recently() returns False for polls whose pub_date is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_poll = Poll(pub_date = time)
        self.assertIs(old_poll.was_published_recently(),False)

    def test_was_published_recently_with_recent_pub_date(self):
        """
        Test whether was_published_recently() returns True for polls whose pub_date is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_poll = Poll(pub_date = time)
        self.assertIs(recent_poll.was_published_recently(),True)

def create_poll(poll_text, days):
    """
    Create a poll with the given `poll_text` and published the
    given number of `days` offset to now (negative for polls published
    in the past, positive for polls that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Poll.objects.create(poll_text=poll_text, pub_date=time)


class pollIndexViewTests(TestCase):
    def test_no_polls(self):
        """
        If no polls exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_poll_list'], [])

    def test_past_poll(self):
        """
        polls with a pub_date in the past are displayed on the
        index page.
        """
        poll = create_poll(poll_text="Past poll.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_poll_list'],
            [poll],
        )

    def test_future_poll(self):
        """
        polls with a pub_date in the future aren't displayed on
        the index page.
        """
        create_poll(poll_text="Future poll.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_poll_list'], [])

    def test_future_poll_and_past_poll(self):
        """
        Even if both past and future polls exist, only past polls
        are displayed.
        """
        poll = create_poll(poll_text="Past poll.", days=-30)
        create_poll(poll_text="Future poll.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_poll_list'],
            [poll],
        )

    def test_two_past_polls(self):
        """
        The polls index page may display multiple polls.
        """
        poll1 = create_poll(poll_text="Past poll 1.", days=-30)
        poll2 = create_poll(poll_text="Past poll 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_poll_list'],
            [poll2, poll1],
        )

class pollDetailViewTests(TestCase):
    def test_future_poll(self):
        """
        The detail view of a poll with a pub_date in the future
        returns a 404 not found.
        """
        future_poll = create_poll(poll_text='Future poll.', days=5)
        url = reverse('polls:detail', args=(future_poll.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_poll(self):
        """
        The detail view of a poll with a pub_date in the past
        displays the poll's text.
        """
        past_poll = create_poll(poll_text='Past poll.', days=-5)
        url = reverse('polls:detail', args=(past_poll.id,))
        response = self.client.get(url)
        self.assertContains(response, past_poll.poll_text)