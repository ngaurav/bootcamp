from __future__ import unicode_literals

import json

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.utils.encoding import python_2_unicode_compatible
from django.utils.html import escape
from django.utils.translation import ugettext_lazy as _

import bleach

from channels import Group

from bootcamp.activities.models import Activity


@python_2_unicode_compatible
class Feed(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    post = models.TextField(max_length=255)
    parent = models.ForeignKey(
        'Feed', null=True, blank=True, on_delete=models.SET_NULL)
    shared_feed = models.ForeignKey(
        'Feed', null=True, blank=True, related_name='SharedFeed+', on_delete=models.SET_NULL)
    likes = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    shares = models.IntegerField(default=0)

    class Meta:
        verbose_name = _('Feed')
        verbose_name_plural = _('Feeds')
        ordering = ('-date',)

    def __str__(self):
        return self.post

    @staticmethod
    def get_feeds(from_feed=None):
        if from_feed is not None:
            feeds = Feed.objects.filter(parent=None, id__lte=from_feed)

        else:
            feeds = Feed.objects.filter(parent=None)

        return feeds

    @staticmethod
    def get_feeds_after(feed):
        feeds = Feed.objects.filter(parent=None, id__gt=feed)
        return feeds

    def get_comments(self):
        return Feed.objects.filter(parent=self).order_by('date')

    def calculate_likes(self):
        likes = Activity.objects.filter(activity_type=Activity.LIKE,
                                        feed=self.pk).count()
        self.likes = likes
        self.save()
        return self.likes

    def get_likes(self):
        likes = Activity.objects.filter(activity_type=Activity.LIKE,
                                        feed=self.pk)
        return likes

    def get_likers(self):
        likes = self.get_likes()
        likers = []
        for like in likes:
            likers.append(like.user)

        return likers

    def calculate_comments(self):
        self.comments = Feed.objects.filter(parent=self).count()
        self.save()
        return self.comments

    def calculate_shares(self):
        self.shares = Feed.objects.filter(shared_feed=self).count()
        self.save()
        return self.shares

    def comment(self, user, post):
        feed_comment = Feed(user=user, post=post, parent=self)
        feed_comment.save()
        self.comments = Feed.objects.filter(parent=self).count()
        self.save()
        return feed_comment

    def share(self, user, post):
        post = post
        if self.shared_feed is None:
            feed_share = Feed(user=user, post=post, shared_feed=self)
        else:
            feed_share = Feed(user=user, post=post, shared_feed=self.shared_feed)
        feed_share.save()
        return feed_share

    def linkfy_post(self):
        return bleach.linkify(escape(self.post))

    def feed_log(self, activity):
        Group('feeds').send({
            'text': json.dumps({
                'username': self.user.username,
                'activity': activity,
            })
        })


def new_feed_added(sender, instance, created, **kwargs):
    if created:
        if instance.parent is None or instance.parent == "":
            instance.feed_log('new_feed')


post_save.connect(new_feed_added, sender=Feed)

class InputFile(models.Model):
    feed = models.ForeignKey(Feed, related_name='files')
    input_file = models.FileField(max_length=1023, upload_to='input_file')

    def __str__(self):
        return self.input_file.__str__()