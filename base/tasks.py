from celery import shared_task
from celery.utils.log import get_task_logger

import jdatetime

from users.models import Profile
from .utils import send_birthday_sms


logger = get_task_logger(__name__)


@shared_task
def every_monday_morning():
    # TODO change birth_date field to date field in models
    for user in Profile.objects.all():
        birth_date = user.birth_date
        try:
            if '-' in birth_date:
                year, month, day = birth_date.split('-')
            elif '/' in birth_date:
                year, month, day = birth_date.split('/')

        except (ValueError, TypeError):
            continue

        year = int(year)
        month = int(month)
        day = int(day)

        current_date = jdatetime.date.today()
        if day == current_date.day and month == current_date.month:
            users_name = user.user.get_full_name() + ' عزیز'
            if users_name is None or users_name == ' عزیز':
                # checks if user have firstname and last name, if string is عزیز then users_name is empty string
                users_name = 'مشتری عزیز'
            send_birthday_sms(name=users_name, mobile='09300629575')
