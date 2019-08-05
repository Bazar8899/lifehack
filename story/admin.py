from django.contrib import admin
from .models import Story, StoryStep, Content, Answer, Question 
from django.forms.models import BaseInlineFormSet
from django.utils.safestring import mark_safe
from django import forms


class StoryAdmin(admin.ModelAdmin):

    empty_value_display = 'Сонгоно уу'

    list_max_show_all = 100

    list_per_page = 50

    list_display = ('id', 'name', 'character', 'order_num', 'is_publish',)

    list_display_links = ('name', )

    fieldsets = (
        (None, {
            'fields': ('name', 'character', 'order_num', 'is_publish',)
        }),
    )

    search_fields = ['name',]

admin.site.register(Story, StoryAdmin)


class StepAdmin(admin.ModelAdmin):

    empty_value_display = '-'

    list_max_show_all = 100

    list_per_page = 50

    list_display = ('id', 'next_step', 'prev_step', 'story', 'name', 'background_image',)

    list_display_links = ('name', )
    ordering = ('name', )

    fieldsets = (
        (None, {
            'fields': ('story', 'name', 'background', 'background_image', 'order_num','next_step', 'prev_step')
        }),
    )

    search_fields = ['story', 'name', 'next_step', 'prev_step']

    readonly_fields = ["background_image", ]

    def background_image(self, obj):
        return mark_safe('<img src="{url}" width="auto" height="100" />'.format(
            url = obj.background.url,
            width=obj.background.width,
            height=obj.background.height,
            )
    )

admin.site.register(StoryStep, StepAdmin)


class ContentAdmin(admin.ModelAdmin):

    empty_value_display = '-'

    list_max_show_all = 100

    list_per_page = 10

    list_display = ('id', 
                    'step', 
                    'content_name',
                    'type', 
                    'position', 
                    'question',
                    # 'content',
                    'bubble_type', 
                    'width',
                    'height',
                    'direction', 
                    'bg_color', 
                    'text_color',)

    list_display_links = ('id', 'content_name',)

    def get_form(self, request, obj=None, **kwargs):
        form = super(ContentAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['step'].label_from_instance = lambda obj: "{} {}".format(obj.id, obj.name)
        return form

    fieldsets = (
        (None, {
            'fields': ('step', 
                       'type', 
                       'question', 
                       'position', 
                       'bubble_type', 
                       'width',
                       'height',
                       'content_name', 
                       'content_image_s',
                       'content_image_m',
                       'content_image_l',
                       'content',
                       'character',
                       'direction', 
                       'bg_color', 
                       'text_color',)
        }),
    )

    search_fields = ['position', 'content_name', 'content', "character",'type', 'bubble_type', 'width', 'height', 'direction', 'bg_color', 'text_color']

    readonly_fields = ["character", ]

    def character(self, obj):
        return mark_safe('<img src="{url}" width="auto" height="100" />'.format(
            url = obj.content_image_s.url,
            width=obj.content_image_s.width,
            height=obj.content_image_s.height,
            )
    )

admin.site.register(Content, ContentAdmin)


class AnswerAdmin(admin.ModelAdmin):

    empty_value_display = 'Сонгоно уу'

    list_max_show_all = 100

    list_per_page = 10

    list_display = ('id', 'answer', 'question', 'step')

    list_display_links = ('id', 'answer', 'question', )

    def get_form(self, request, obj=None, **kwargs):
        form = super(AnswerAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['question'].label_from_instance = lambda obj: "{} {}".format(obj.id, obj.question)
        return form

    fieldsets = (
        (None, {
            'fields': ('question', 'answer', 'step')
        }),
    )

    search_fields = ['answer', 'question',]

admin.site.register(Answer, AnswerAdmin)


class QuestionAdmin(admin.ModelAdmin):

    empty_value_display = 'Сонгоно уу'

    list_max_show_all = 100

    list_per_page = 50

    list_display = ('id', 'question', 'text')

    list_display_links = ('id', 'question', 'text')

    fieldsets = (
        (None, {
            'fields': ('question', 'order_num', 'text')
        }),
    )

    search_fields = [ 'question',]

admin.site.register(Question, QuestionAdmin)