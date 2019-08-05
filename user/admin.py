from django.contrib import admin
from .models import LHUser, CharacterImage, Character

from django.forms.models import BaseInlineFormSet
from django.utils.safestring import mark_safe

# User admin register
class LHUserAdmin(admin.ModelAdmin):

    empty_value_display = '-'

    list_max_show_all = 100

    list_per_page = 50

    list_display = ('id', 'username', 'first_name', 'last_name', 'dob', 'gender', 'device_id', 'email',)

    list_display_links = ('username', 'id')

    fieldsets = (
        (None, {
            'fields': ('first_name', 'last_name', 'username', 'dob', 'gender', 'device_id', 'email')
        }),
    )

    search_fields = ['gender', 'first_name', 'last_name']

admin.site.register(LHUser, LHUserAdmin)

class RequiredInlineFormSet(BaseInlineFormSet):
    def _construct_form(self, i, **kwargs):
        form = super(RequiredInlineFormSet, self)._construct_form(i, **kwargs)
        if i < 1:
            form.empty_permitted = False
        return form

class CharacterImageInline(admin.TabularInline):

    model = CharacterImage

    fieldsets = (
        (None, {
            'fields': ('image_s', 'image_m', 'image_l', 'character_image')
        }),
    )

    extra = 1
    formset = RequiredInlineFormSet

    readonly_fields = ["character_image", ]

    def character_image(self, obj):
        return mark_safe('<img src="{url}" width="auto" height="100" />'.format(
            url = obj.image_s.url,
            width=obj.image_s.width,
            height=obj.image_s.height,
            )
    )

# admin.site.register(CharacterImage, CharacterImageInline)

class CharacterAdmin(admin.ModelAdmin):
    inlines = [
        CharacterImageInline
    ]

    model = Character

    list_display = ('name', 'age', 'gender', 'avatar_img_s', 'character_type',)

    fieldsets = (
        (None, {
            'fields': ('name', 'age', 'gender', 'avatar', 'avatar_img_s', 'avatar_img_m', 'avatar_img_l', 'character_type',)
        }),
    )

    readonly_fields = ["avatar", ]

    def avatar(self, obj):
        return mark_safe('<img src="{url}" width="auto" height="100" />'.format(
            url = obj.avatar_img_s.url,
            width=obj.avatar_img_s.width,
            height=obj.avatar_img_s.height,
            )
    )

admin.site.register(Character, CharacterAdmin)
