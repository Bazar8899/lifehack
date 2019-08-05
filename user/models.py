from django.db import models
from django.contrib.auth.models import AbstractUser
from lifeHack.models import BaseModel
from django.utils.timezone import now
from django.utils.html import format_html
from oauth2_provider.models import AbstractApplication

# Create your models here.


class LHUser(AbstractUser):

    GENDERS = (
        (0, 'Эмэгтэй'),
        (1, 'Эрэгтэй'),
        (2, 'Аль нь ч биш'),
    )

    dob = models.IntegerField(default=0, verbose_name="Төрсөн он")
    gender = models.IntegerField(default=0, choices=GENDERS , verbose_name="Хүйс")
    device_id = models.CharField(default='', max_length=100, verbose_name="Гар утасны id")
    username = models.CharField(default='', max_length=100, verbose_name="Нэвтрэх нэр")
    last_name = models.CharField(default='', max_length=100, blank=True, verbose_name="Овог")
    first_name = models.CharField(default='', max_length=100, blank=True, verbose_name="Нэр")
    profile_img = models.ImageField(upload_to="media/profile", verbose_name="Profile image", default=None)

    def __str__(self):
        return self.username


class Character(BaseModel):
    
    GENDERS = (
        (0, 'Эмэгтэй'),
        (1, 'Эрэгтэй'),
        (2, 'Аль нь ч биш'),
    )

    CHARACTER_TYPE = (
        (0, 'Straight'),
        (1, 'Lesbian'),
        (2, 'Gay'),
        (3, 'Transgender'),
    )

    avatar_img_s = models.ImageField(upload_to="media/character/avatar_s", verbose_name="Character avatar 1x", default=None)
    avatar_img_m = models.ImageField(upload_to="media/character/avatar_m", verbose_name="Character avatar 2x", default=None)
    avatar_img_l = models.ImageField(upload_to="media/character/avatar_l", verbose_name="Character avatar 3x", default=None)
    name = models.CharField(max_length=100, default=None, verbose_name="Дүрийн нэр")
    age = models.IntegerField(default=None, verbose_name='Age')
    gender = models.IntegerField(default=None, choices=GENDERS, verbose_name='Gender')
    character_type = models.IntegerField(default=None, choices=CHARACTER_TYPE,verbose_name='Character type')

    def __str__(self):
        return self.name


class CharacterImage(BaseModel):

    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name="characterimage_character", default=None)
    image_s = models.ImageField(upload_to="media/character", verbose_name="Character Image 1x", default=None)
    image_m = models.ImageField(upload_to="media/character", verbose_name="Character Image 2x", default=None)
    image_l = models.ImageField(upload_to="media/character", verbose_name="Character Image 3x", default=None)
    

class LifeHackOAuthApplication(AbstractApplication):
    is_local = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'oApplication'
        verbose_name_plural = 'oApplications'

