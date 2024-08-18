from email.policy import default

from django.core.exceptions import BadRequest
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from django_ratelimit.decorators import ratelimit
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from seinfeld.filters import SentenceFilter
from seinfeld.models import Utterance, Sentence
from seinfeld.serializers import (
    SentenceSerializer,
    UtteranceSerializer,
)
from seinfeld.util.open_ai import AIConversation

from seinfeld.util.util import get_random_from_queryset


class Pagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class QuoteViewSet(ReadOnlyModelViewSet):
    model = Sentence
    queryset = Sentence.objects.all()
    serializer_class = SentenceSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = SentenceFilter
    pagination_class = Pagination

    @method_decorator(ratelimit(key="ip", rate="30/h", method="GET", block=True))
    @method_decorator(cache_page(None))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @method_decorator(ratelimit(key="ip", rate="30/h", method="GET", block=True))
    @method_decorator(cache_page(None))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(ratelimit(key="ip", rate="30/h", method="GET", block=True))
    @action(detail=False, methods=["GET"])
    def random(self, request):
        return Response(
            self.get_serializer(get_random_from_queryset(self.get_queryset())).data,
        )


class UtteranceViewSet(ReadOnlyModelViewSet):
    model = Utterance
    queryset = Utterance.manager.all()
    serializer_class = UtteranceSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = SentenceFilter
    pagination_class = Pagination

    @method_decorator(ratelimit(key="ip", rate="30/h", method="GET", block=True))
    @method_decorator(cache_page(None))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @method_decorator(ratelimit(key="ip", rate="30/h", method="GET", block=True))
    @method_decorator(cache_page(None))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

class ConversationView(APIView):
    def post(self, request):

        speaker = request.data.get('speaker').upper()
        season = request.data.get('season')
        episode = request.data.get('episode')
        user_input = request.data.get('user_input')


        open_api = AIConversation(
            speaker=speaker,
            season=season,
            episode=episode,
        )

        output = open_api.chat(user_input)


        return Response(output)
