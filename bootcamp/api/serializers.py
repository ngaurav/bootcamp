from django.contrib.auth.models import User, Group
from rest_framework import serializers

from bootcamp.activities.models import Activity, Notification
from bootcamp.articles.models import Article, ArticleComment
from bootcamp.authentication.models import Profile
from bootcamp.feeds.models import Feed
from bootcamp.messenger.models import Message
from bootcamp.questions.models import Question, Answer


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class FeedSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Feed
        fields = ('user', 'date', 'parent', 'likes', 'comments')


class ActivitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Activity
        fields = ('user', 'activity_type', 'date', 'feed', 'question', 'answer')
