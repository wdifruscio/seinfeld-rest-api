# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.db.models import Count, Max
from django.db.models.functions.text import Length


class Episode(models.Model):
    season_number = models.IntegerField()
    episode_number = models.IntegerField()
    title = models.TextField(blank=True, null=True)
    the_date = models.TextField(blank=True, null=True)
    writer = models.TextField(blank=True, null=True)
    director = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'episode'


class Sentence(models.Model):
    utterance = models.ForeignKey('Utterance', models.DO_NOTHING)
    sentence_number = models.IntegerField()
    text = models.TextField()

    class Meta:
        managed = False
        db_table = 'sentence'


class Utterance(models.Model):
    episode = models.ForeignKey(Episode, models.DO_NOTHING)
    utterance_number = models.IntegerField()
    speaker = models.TextField()

    class Meta:
        managed = False
        db_table = 'utterance'

    # sentence set works
    def get_sentences(self):
        return Sentence.objects.filter(utterance=self.utterance_number)

    def get_one_liner_by_length(self, length=150):
        return Utterance.objects.annotate(
            sentence_count=Count('sentence'),
            max_sentence_length=Max(Length('sentence__text'))
        ).filter(sentence_count=1, max_sentence_length__gt=length)


class Word(models.Model):
    sentence = models.ForeignKey(Sentence, models.DO_NOTHING)
    word_number = models.IntegerField()
    text = models.TextField()
    part_of_speech = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'word'
