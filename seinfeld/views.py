from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet

from seinfeld.filters import SentenceFilter
from seinfeld.models import Utterance, Sentence
from seinfeld.serializers import SentenceSerializer
from seinfeld.util import get_random_from_queryset


class QuoteViewSet(ReadOnlyModelViewSet):
    model = Sentence
    queryset = Sentence.objects.all()
    serializer_class = SentenceSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = SentenceFilter
    pagination_class = PageNumberPagination

    @action(detail=False, methods=["GET"])
    def random(self, request):
        return Response(
            self.get_serializer(get_random_from_queryset(self.get_queryset())).data,
        )

class ConversationViewSet(GenericViewSet):
    model = Sentence
    queryset = Sentence.objects.all()
    lookup_field = 'utterance_id'
    serializer_class = SentenceSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = SentenceFilter
    pagination_class = PageNumberPagination

    def list(self, request, *args, **kwargs):
        #need aggregation query
        sentences = Sentence.objects.aggregate()

    def retrieve(self, request, *args, **kwargs):
        sentences = Sentence.objects.filter(utterance_id=kwargs['utterance_id'])
        return Response(
            self.get_serializer(sentences, many=True).data
        )




