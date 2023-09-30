from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import Profile


@receiver(post_save, sender=Profile)
def create_user_profile(sender, instance, created, **kwargs):
    try:
        if created:
            pass
        else:
            if hasattr(instance, '_dirty'):
                return

            completed_percent = 0
            if instance.role == '1':
                if instance.private.fname:
                    completed_percent += 11.11
                if instance.private.lname:
                    completed_percent += 11.11
                if instance.mobile:
                    completed_percent += 11.11
                if instance.private.id_code:
                    completed_percent += 11.11
                if instance.birth_date:
                    completed_percent += 11.11
                if instance.state:
                    completed_percent += 11.11
                if instance.city:
                    completed_percent += 11.11
                if instance.address:
                    completed_percent += 11.11
                if instance.zipcode:
                    completed_percent += 11.11
                instance.completed_percent = round(completed_percent)
            try:
                instance._dirty = True
                instance.save()
            finally:
                del instance._dirty
    except Exception as e:
        pass