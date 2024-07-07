from django.db.models import Manager, Count, Max
from django.db.models.functions import Length


class UtteranceManager(Manager):
    def get_first_sentence_by_length(self, length=100):
        return self.annotate(
            sentence_count=Count("sentence"),
            max_sentence_length=Max(Length("sentence__text")),
        ).filter(sentence_count=1, max_sentence_length__gt=length)
