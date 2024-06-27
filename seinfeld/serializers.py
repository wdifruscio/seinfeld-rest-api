from rest_framework import serializers

from seinfeld.models import Utterance, Sentence
class QuoteSerializer(serializers.Serializer):
    text = serializers.SerializerMethodField()
    speaker = serializers.CharField()
    season_number = serializers.SerializerMethodField()
    episode_number = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    the_date = serializers.SerializerMethodField()
    writer = serializers.SerializerMethodField()
    director = serializers.SerializerMethodField()

    def get_text(self, obj):
        return obj.sentence_set.first().text

    def get_season_number(self,obj):
        return obj.episode.season_number
    def get_episode_number(self,obj):
        return obj.episode.episode_number
    def get_title(self,obj):
        return obj.episode.title
    def get_the_date(self,obj):
        return obj.episode.the_date
    def get_writer(self,obj):
        return obj.episode.writer
    def get_director(self,obj):
        return obj.episode.director
