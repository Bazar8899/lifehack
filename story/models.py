import calendar

from django.db import models
from user.models import Character, LHUser

# Create by Bazar.


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

class Question(BaseModel):
    question = models.CharField(default=None, max_length=500)
    text = models.CharField(default=None, max_length=500)
    order_num = models.IntegerField(default=None)

    def __str__(self):
        return self.question


class Story(BaseModel):

    is_publish = (
        (0, 'Un publish'),
        (1, 'Publish'),
    )

    name = models.CharField(default=None, max_length=250, verbose_name="Түүхийн нэр")
    avatar = models.ImageField(upload_to="media/character", verbose_name="Avatar", default=None)
    character = models.ForeignKey(Character, default=None, on_delete=models.CASCADE, verbose_name='Character')
    order_num = models.IntegerField(default=0, verbose_name="Дараалал")
    is_publish = models.IntegerField(choices=is_publish, default=0)

    def __str__(self):
        return self.name


class StoryStep (BaseModel):

    name = models.CharField(max_length=100, default=None, verbose_name="Дэлгэцийн нэр")
    story = models.ForeignKey(Story, on_delete=models.CASCADE, verbose_name="Түүх")
    background = models.ImageField(upload_to="media/character", verbose_name="Background Image", default=None)
    order_num = models.IntegerField(default=0, verbose_name='Order num')
    next_step = models.IntegerField(default=0, verbose_name='Next step')
    prev_step = models.IntegerField(default=0, verbose_name='Prev step')

    def __str__(self):
        return self.name


class Answer(BaseModel):
    question = models.ForeignKey(Question, default=None, verbose_name="Question", on_delete=models.CASCADE)
    answer = models.CharField(default=None, max_length=500)
    step = models.ForeignKey(StoryStep, default=None, verbose_name="Step", on_delete=models.CASCADE)

    def __str__(self):
        return self.answer


class Content (BaseModel):
    
    POSITION = (
        (0, '--'),
        (10, 'Top'),
        (11, 'Top left'),
        (12, 'Top right'),

        (20, 'Middle'),
        (21, 'Middle left'),
        (22, 'Middle right'),
        
        (30, 'Middle top'),
        (31, 'Middle top left'),
        (32, 'Middle top right'),
        
        (40, 'Middle bottom'),
        (41, 'Middle bottom left'),
        (42, 'Middle bottom right'),

        (50, 'Bottom'),
        (51, 'Bottom left'),
        (52, 'Bottom right'),

        (60, 'Character 1'),
        (61, 'Character 2'),
        (62, 'Character 3'),
        (63, 'Character 4'),
    )

    TYPE = (
        (0, '--'),
        (1, 'Bubble'),
        (2, 'Question'),
        (3, 'Character'),
        (4, 'Transition'),
        (5, 'Button'),
    )

    WIDTH = (
        (1, 'Small'),
        (2, 'Medium'),
        (3, 'Big'),
    )

    HEIGHT = (
        (0, 'Short'),
        (1, 'Tall'),
    )

    DIRECTION = (
        (0, '--'),
        (1, 'To left'),
        (2, 'To right'),
        (3, 'To top'),
        (4, 'To bottom'),
    )

    TRANSITION = (
        (0, '--'),
        (1, 'Fade'),
        (2, 'Slide to left'),
        (3, 'Slide to right'),
        (4, 'Slide to top'),
        (5, 'Slide to bottom'),
    )

    BUBBLE_TYPE = ( #TextBox-iin arrow chiglel
        (0, '--'),
        (1, 'Top'),
        (2, 'Bottom'),
        
        (3, 'Left'),
        (4, 'Left top'),
        (5, 'Left bottom'),

        (6, 'Right'),
        (7, 'Right top'),
        (8, 'Right bottom'),
    )

    type = models.IntegerField(choices=TYPE, default=0)
    position = models.IntegerField(default=0, verbose_name="Position", choices=POSITION)
    transition = models.IntegerField(default=0, choices=TRANSITION)
    width = models.IntegerField(choices=WIDTH, default=0, verbose_name='Text box width')
    height = models.IntegerField(choices=HEIGHT, default=0)
    direction = models.IntegerField(choices=DIRECTION, default=0)
    
    bg_color = models.CharField(default=None, max_length=10, null=True, blank=True, verbose_name="Background color")
    text_color = models.CharField(default=None, max_length=10, null=True, blank=True, verbose_name="Text Color")
    color = models.CharField(default=None, max_length=100, null=True, blank=True )

    bubble_type = models.IntegerField(default=0, choices=BUBBLE_TYPE)

    step = models.ForeignKey(StoryStep, default=None, verbose_name="Step", on_delete=models.CASCADE)
    
    content_name = models.CharField(max_length=100, default=None, verbose_name="Content name")
    content_image_s = models.ImageField(upload_to="media/character_image", verbose_name="Character Image 1x", default=None, null=True, blank=True)
    content_image_m = models.ImageField(upload_to="media/character_image", verbose_name="Character Image 2x", default=None, null=True, blank=True)
    content_image_l = models.ImageField(upload_to="media/character_image", verbose_name="Character Image 3x", default=None, null=True, blank=True)
    content = models.CharField(default='', max_length=2000, verbose_name="Content text")
    question = models.ForeignKey(Question, default=None, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Question")

    def __str__(self):
        return self.content_name

    
class UserStory(BaseModel):
    user = models.ForeignKey(LHUser, on_delete=models.CASCADE)
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    step = models.ForeignKey(StoryStep, on_delete=models.CASCADE, default=None, null=True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, default=None, null=True)
    type = models.IntegerField(default=0, verbose_name='Log type')

