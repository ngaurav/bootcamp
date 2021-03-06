from __future__ import unicode_literals
import json

from django.db.models.functions import TruncMonth, TruncDay
from django.db.models import Count

from django.contrib.auth.models import User
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.html import escape


@python_2_unicode_compatible
class Activity(models.Model):
    LIKE = 'L'
    ACTIVITY_TYPES = (
        (LIKE, 'Like'),
        )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=1, choices=ACTIVITY_TYPES)
    date = models.DateTimeField(auto_now_add=True)
    feed = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = 'Activity'
        verbose_name_plural = 'Activities'

    @staticmethod
    def monthly_activity(user):
        """Static method to retrieve monthly statistical information about the
        user activity.
        @requires:  user - Instance from the User Django model.
        @returns:   Two JSON arrays, the first one is dates which contains all
                    the dates with activity records, and the second one is
                    datapoints containing the sum of all the activity than had
                    place in every single month.

        Both arrays keep the same order, so there is no need to order them.
        """
        # months = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        # "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        query = Activity.objects.filter(user=user).annotate(
            month=TruncMonth('date')).values('month').annotate(
                c=Count('id')).values('month', 'c')
        try:
            dates, datapoints = zip(
                *[[a['c'], str(a['month'].date())] for a in query])
            return json.dumps(dates), json.dumps(datapoints)

        except ValueError:
            return json.dumps(0), json.dumps(0)

    @staticmethod
    def daily_activity(user):
        """Static method to retrieve daily statistical information about the
        user activity.
        @requires:  user - Instance from the User Django model.
        @returns:   Two JSON arrays, the first one is dates which contains all
                    the dates with activity records, and the second one is
                    datapoints containing the sum of all the activity than had
                    place in every single day.

        Both arrays keep the same order, so there is no need to order them.
        """
        query = Activity.objects.filter(user=user).annotate(day=TruncDay(
            'date')).values('day').annotate(c=Count('id')).values('day', 'c')
        try:
            dates, datapoints = zip(
                *[[a['c'], str(a['day'].date())] for a in query])
            return json.dumps(dates), json.dumps(datapoints)

        except ValueError:
            return json.dumps(0), json.dumps(0)

    def __str__(self):
        return self.activity_type


@python_2_unicode_compatible
class Notification(models.Model):
    LIKED = 'L'
    COMMENTED = 'C'
    EDITED_ARTICLE = 'E'
    ALSO_COMMENTED = 'A'
    SHARED = 'S'
    LOGGED_IN = 'I'
    LOGGED_OUT = 'O'
    NOTIFICATION_TYPES = (
        (LIKED, 'Liked'),
        (COMMENTED, 'Commented'),
        (EDITED_ARTICLE, 'Edited Article'),
        (ALSO_COMMENTED, 'Also Commented'),
        (SHARED, 'Shared'),
        (LOGGED_IN, 'Logged In'),
        (LOGGED_OUT, 'Logged Out'),
        )

    # _LIKED_TEMPLATE = '<a href="/{0}/">{1}</a> liked your post: <a href="/feeds/{2}/">{3}</a>'  # noqa: E501
    # _COMMENTED_TEMPLATE = '<a href="/{0}/">{1}</a> commented on your post: <a href="/feeds/{2}/">{3}</a>'  # noqa: E501
    # _EDITED_ARTICLE_TEMPLATE = '<a href="/{0}/">{1}</a> edited your article: <a href="/article/{2}/">{3}</a>'  # noqa: E501
    # _ALSO_COMMENTED_TEMPLATE = '<a href="/{0}/">{1}</a> also commentend on the post: <a href="/feeds/{2}/">{3}</a>'  # noqa: E501
    # _SHARED_TEMPLATE = '<a href="/{0}/">{1}</a> shared your post: <a href="/feeds/{2}/">{3}</a>'  # noqa: E501
    # _USER_LOGIN_TEMPLATE = '<a href="/{0}/">{1}</a> has just logged in.'  # noqa: E501
    # _USER_LOGOUT_TEMPLATE = '<a href="/{0}/">{1}</a> has just logged out.'  # noqa: E501

    _LIKED_TEMPLATE = '<a class="dropdown-item" href="/feeds/{2}/">{1} liked your post: <a href="/feeds/{2}/">{3}</a>'  # noqa: E501
    _COMMENTED_TEMPLATE = '<a class="dropdown-item" href="/feeds/{2}/">{1} commented on your post: <a href="/feeds/{2}/">{3}</a>'  # noqa: E501
    _EDITED_ARTICLE_TEMPLATE = '<a class="dropdown-item" href="/article/{2}/">{1} edited your article: <a href="/article/{2}/">{3}</a>'  # noqa: E501
    _ALSO_COMMENTED_TEMPLATE = '<a class="dropdown-item" href="/feeds/{2}/">{1} also commentend on the post: <a href="/feeds/{2}/">{3}</a>'  # noqa: E501
    _SHARED_TEMPLATE = '<a class="dropdown-item" href="/feeds/{2}/">{1} shared your post.</a>'  # noqa: E501
    _USER_LOGIN_TEMPLATE = '<a class="dropdown-item" href="/{0}/">{1} has just logged in.</a>'  # noqa: E501
    _USER_LOGOUT_TEMPLATE = '<a class="dropdown-item" href="/{0}/">{1} has just logged out.</a>'  # noqa: E501

    from_user = models.ForeignKey(
        User, related_name='+', on_delete=models.CASCADE)
    to_user = models.ForeignKey(
        User, related_name='+', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    feed = models.ForeignKey(
        'feeds.Feed', null=True, blank=True, on_delete=models.CASCADE)
    article = models.ForeignKey(
        'articles.Article', null=True, blank=True, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=1,
                                         choices=NOTIFICATION_TYPES)
    is_read = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ('-date',)

    def __str__(self):
        if self.notification_type == self.LIKED:
            return self._LIKED_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.profile.get_screen_name()),
                self.feed.pk,
                escape(self.get_summary(self.feed.post))
                )

        elif self.notification_type == self.COMMENTED:
            return self._COMMENTED_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.profile.get_screen_name()),
                self.feed.pk,
                escape(self.get_summary(self.feed.post))
                )

        elif self.notification_type == self.EDITED_ARTICLE:
            return self._EDITED_ARTICLE_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.profile.get_screen_name()),
                self.article.slug,
                escape(self.get_summary(self.article.title))
                )

        elif self.notification_type == self.ALSO_COMMENTED:
            return self._ALSO_COMMENTED_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.profile.get_screen_name()),
                self.feed.pk,
                escape(self.get_summary(self.feed.post))
                )

        elif self.notification_type == self.SHARED:
            return self._SHARED_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.profile.get_screen_name()),
                self.feed.pk,
                escape(self.get_summary(self.feed.post))
                )

        elif self.notification_type == self.LOGGED_IN:
            return self._USER_LOGIN_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.profile.get_screen_name())
                )

        elif self.notification_type == self.LOGGED_OUT:
            return self._USER_LOGOUT_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.profile.get_screen_name())
                )

        else:
            return 'Ooops! Something went wrong.'

    def get_summary(self, value):
        summary_size = 50
        if len(value) > summary_size:
            return '{0}...'.format(value[:summary_size])

        else:
            return value

    @staticmethod
    def call_latest_notifications(user):
        notifications = Notification.objects.filter(
            to_user=user, is_read=False) | Notification.objects.filter(
                notification_type__in=['I', 'O'], is_read=False).exclude(
                    from_user=user)
        for notification in notifications:
            notification.is_read = True
            notification.save()

        return notifications[:5]
