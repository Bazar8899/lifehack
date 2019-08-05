from django.db import models

class BaseModelManager(models.Manager):
    def get_queryset(self):
        return super(BaseModelManager, self).get_queryset().filter(deletedAt__isnull=True)

class BaseModel(models.Model):

    """
    Base model
    """
    objects = BaseModelManager()
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deletedAt = models.DateTimeField(null = True)

    def soft_delete(self, *args, **kwargs):

        self.deletedAt = datetime.now()
        self.save()

    class Meta:
        """
        Class meta
        """
        abstract = True
