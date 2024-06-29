from random import randint


def get_random_from_queryset(queryset):
    random_index = randint(0, queryset.count() - 1)
    return queryset[random_index]