from django.contrib.auth.models import User, Group

from rest_framework.serializers import ModelSerializer, HyperlinkedModelSerializer

from bootcamp.authentication.models import Profile
from bootcamp.activities.models import Activity, Notification
from bootcamp.feeds.models import Feed
from bootcamp.articles.models import Article, ArticleComment
from bootcamp.messenger.models import Message
from bootcamp.questions.models import Question, Answer


class UserSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class ActivitySerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Activity
        fields = ('user', 'activity_type', 'date', 'feed', 'question', 'answer')


class FeedSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Feed
        fields = ('user', 'date', 'parent', 'likes', 'comments')


class NotificationSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Notification
        fields = ('from_user', 'to_user', 'date', 'feed', 'question', 'answer',
                  'article', 'notification_type', 'is_read')


class ArticleSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Article
        # TODO: 'tags' is instance of TaggableManager, adding it causes
        # Object of type '_TaggableManager' is not JSON serializable
        fields = ('title', 'slug', 'content', 'status', 'create_user',
                  'create_date', 'update_date', 'update_user')


class ArticleCommentSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = ArticleComment
        fields = ('article', 'comment', 'date', 'user')


class MessageSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Message
        fields = ('user', 'message', 'date', 'conversation', 'from_user',
                  'is_read')