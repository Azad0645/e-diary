import random
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from datacenter.models import Schoolkid, Mark, Chastisement, Commendation, Lesson


def find_schoolkid(full_name):
    try:
        return Schoolkid.objects.get(full_name__icontains=full_name)
    except ObjectDoesNotExist:
        print(f"Ученик с именем '{full_name}' не найден.")
    except MultipleObjectsReturned:
        print(f"Найдено несколько учеников с именем '{full_name}', уточните имя.")
    return None


def fix_marks(schoolkid):
    bad_marks = Mark.objects.filter(schoolkid=schoolkid, points__lt=4)
    bad_marks.update(points=5)
    print(f"Исправлено плохих оценок: {bad_marks.count()}")


def remove_chastisements(schoolkid):
    removed_count, _ = Chastisement.objects.filter(schoolkid=schoolkid).delete()
    print(f"Удалено замечаний: {removed_count}")


def create_commendation(full_name, subject_name):
    kid = find_schoolkid(full_name)
    if not kid:
        return

    lesson = Lesson.objects.filter(
        year_of_study=kid.year_of_study,
        group_letter=kid.group_letter,
        subject__title__icontains=subject_name
    ).order_by('-date').first()

    if not lesson:
        print(f"Урок по предмету '{subject_name}' не найден.")
        return

    commendation_texts = [
        "Молодец!",
        "Отлично справился!",
        "Хорошая работа!",
        "Так держать!",
        "Превосходно!",
        "Очень старался!",
    ]

    Commendation.objects.create(
        text=random.choice(commendation_texts),
        created=lesson.date,
        schoolkid=kid,
        subject=lesson.subject,
        teacher=lesson.teacher
    )
    print(f"Добавлена похвала по предмету '{lesson.subject.title}'")