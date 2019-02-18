from django.db import models

from django.conf import settings
from polls.choices import *


def filter_votes(vote):
    return vote.vote_value


class Poll(models.Model):

    def complexity(self):
        votes = list(map(filter_votes, self.vote_set.all()))
        return round(sum(votes) / len(votes), 2) if len(votes) else "Not Set"

    poll_title = models.CharField(max_length=200)
    poll_description = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='publisher', on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True, blank=True)


class Vote(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='voter', on_delete=models.CASCADE)
    vote_value = models.FloatField(default=0, choices=COMPLEXITY)
    pub_date = models.DateTimeField(auto_now_add=True, blank=True)
