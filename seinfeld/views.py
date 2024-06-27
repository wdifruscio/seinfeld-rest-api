from random import randint

import django.core.paginator
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from seinfeld.models import Utterance
from seinfeld.serializers import QuoteSerializer


class QuoteViewSet(GenericViewSet):
    model = Utterance
    queryset = Utterance.manager.all()
    # pagination_class = django.core.paginator.Paginator

    @action(detail=False, methods=['GET'])
    @method_decorator(ratelimit(key='ip', rate='10/m', method='GET'))
    def random(self, request, *args, **kwargs):
        queryset = Utterance.manager.get_one_liner_by_length()
        random_index = randint(0, queryset.count() - 1)
        random_utterance = queryset[random_index]
        serializer = QuoteSerializer(random_utterance)
        return Response(serializer.data, status=status.HTTP_200_OK)
