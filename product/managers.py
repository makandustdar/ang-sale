from django.db.models import Manager


class ActivesManager(Manager):
    def get_queryset(self):
        return super(ActivesManager, self).get_queryset().filter(
            isActive=True
        )
