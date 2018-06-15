from typing import Union, Dict

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User, Group
from django.http import HttpRequest

from rest_framework import status
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.request import Request as RestRequest
from rest_framework.response import Response as RestResponse
from rest_framework.renderers import JSONRenderer

from bootcamp.activities.models import Activity, Notification
from bootcamp.articles.models import Article, ArticleComment
from bootcamp.authentication.models import Profile
from bootcamp.feeds.models import Feed
from bootcamp.messenger.models import Message
from bootcamp.questions.models import Question, Answer

from bootcamp.api.serializers import UserSerializer
from bootcamp.api.serializers import ActivitySerializer
from bootcamp.api.serializers import NotificationSerializer
from bootcamp.api import serializers


class GenericFeedViewSet(generics.ListCreateAPIView,
                         generics.RetrieveAPIView,
                         viewsets.ViewSet):
    queryset = Feed.objects.all()
    serializer_class = serializers.FeedSerializer


class GenericNotificationViewSet(generics.ListCreateAPIView,
                                 viewsets.ViewSet):
    queryset = Notification.objects.all()
    serializer_class = serializers.NotificationSerializer


class GenericActivityListViewSet(generics.RetrieveUpdateAPIView,
                                 generics.ListCreateAPIView,
                                 viewsets.ViewSet):
    queryset = Activity.objects.all()
    serializer_class = serializers.ActivitySerializer


class GenericNotificationListViewSet(generics.RetrieveUpdateAPIView,
                                     generics.ListCreateAPIView,
                                     viewsets.ViewSet):
    queryset = Notification.objects.all()
    serializer_class = serializers.NotificationSerializer


class GenericArticleViewSet(generics.ListCreateAPIView,
                            generics.RetrieveUpdateDestroyAPIView,
                            viewsets.ViewSet):
    queryset = Article.objects.all()
    serializer_class = serializers.ArticleSerializer


class GenericArticleCommentViewSet(generics.ListCreateAPIView,
                                   generics.RetrieveUpdateDestroyAPIView,
                                   viewsets.ViewSet):
    queryset = ArticleComment.objects.all()
    serializer_class = serializers.ArticleCommentSerializer


class GenericMessageViewSet(generics.ListCreateAPIView,
                            generics.RetrieveUpdateDestroyAPIView,
                            viewsets.ViewSet):
    queryset = Message.objects.all()
    serializer_class = serializers.MessageSerializer


class GenericQuestionViewSet(generics.ListCreateAPIView,
                             generics.RetrieveUpdateDestroyAPIView,
                             viewsets.ViewSet):
    queryset = Question.objects.all()
    serializer_class = serializers.QuestionSerializer


class GenericAnswerViewSet(generics.ListCreateAPIView,
                           generics.RetrieveUpdateDestroyAPIView,
                           viewsets.ViewSet):
    queryset = Answer.objects.all()
    serializer_class = serializers.AnswerSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class ActivityViewSet(viewsets.ModelViewSet):
    """
    API endpoint for activities.
    """
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer


def context(request: RestRequest) -> Dict:
    """
    Creates a context dict for the serializers.

    See https://stackoverflow.com/a/34444082
    """
    r = RestRequest(request._request)
    r.accepted_renderer = JSONRenderer
    return {'request': r}


# TODO: DEPRECATED
@api_view(['GET', 'POST'])
@renderer_classes((JSONRenderer,))
@csrf_exempt
def user_list(request: RestRequest) -> RestResponse:
    """
    List all users, or create a new one.
    """
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, context=context(request), many=True)
        # TODO: what is happening here with RestResponse, the decorators get mangled up...
        return RestResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return RestResponse(serializer.data, status=status.HTTP_201_CREATED)
        return RestResponse(serializer.errors, status=status.HTTP_404_NOT_FOUND)


# TODO: DEPRECATED
@csrf_exempt
def user_detail(request: RestRequest, pk: Union[int, str]) -> Union[HttpResponse, JsonResponse]:
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = UserSerializer(user, context=context(request))
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = UserSerializer(user, context=context(request), data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        user.delete()
        return HttpResponse(status=204)
