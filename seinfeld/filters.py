from django.db.models import Max
from django.db.models.functions import Length
from django_filters import FilterSet, filters


class SentenceFilter(FilterSet):
    speaker = filters.CharFilter(method="filter_speaker")
    episode_id = filters.CharFilter(method="filter_episode")
    season = filters.CharFilter(method="filter_season")
    writer = filters.CharFilter(method="filter_writer")
    director = filters.CharFilter(method="filter_director")
    title = filters.CharFilter(method="filter_title")
    length = filters.CharFilter(method="filter_length")
    search = filters.CharFilter(method="filter_search")

    def filter_search(self, queryset, name, value):
        return queryset.filter(text__icontains=str.lower(value))

    def filter_length(self, queryset, name, value):
        return queryset.annotate(max_length=Max(Length("text"))).filter(
            max_length__gt=value
        )

    def filter_speaker(self, queryset, name, value):
        return queryset.filter(utterance__speaker=str.upper(value))

    def filter_episode_id(self, queryset, name, value):
        return queryset.filter(utterance__episode=value)

    def filter_season(self, queryset, name, value):
        return queryset.filter(utterance__episode__season=value)

    def filter_writer(self, queryset, name, value):
        return queryset.filter(utterance__episode__writer=value)

    def filter_director(self, queryset, name, value):
        return queryset.filter(utterance__episode__director=value)

    def filter_title(self, queryset, name, value):
        return queryset.filter(utterance__episode__title=value)
