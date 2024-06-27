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

from seinfeld.managers import UtteranceManager


class IdModel(models.Model):
    id = models.IntegerField(primary_key=True)

    class Meta:
        abstract = True


class Episode(IdModel):
    season_number = models.IntegerField()
    episode_number = models.IntegerField()
    title = models.TextField(blank=True, null=True)
    the_date = models.TextField(blank=True, null=True)
    writer = models.TextField(blank=True, null=True)
    director = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'episode'


class Sentence(IdModel):
    utterance = models.ForeignKey('Utterance', models.DO_NOTHING)
    sentence_number = models.IntegerField()
    text = models.TextField()

    class Meta:
        managed = False
        db_table = 'sentence'


class Utterance(IdModel):
    episode = models.ForeignKey(Episode, models.DO_NOTHING)
    utterance_number = models.IntegerField()
    speaker = models.TextField()

    manager = UtteranceManager()

    class Meta:
        managed = False
        db_table = 'utterance'




class Word(IdModel):
    sentence = models.ForeignKey(Sentence, models.DO_NOTHING)
    word_number = models.IntegerField()
    text = models.TextField()
    part_of_speech = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'word'
