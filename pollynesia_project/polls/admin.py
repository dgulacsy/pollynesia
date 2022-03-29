from django.contrib import admin

from .models import Choice, Poll

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class PollAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,{'fields': ['title','description']}),
        ('Location',{'fields':['location']}),
        ('Date information', {'fields': ['pub_date','open_from','close_at'], 'classes': ['collapse']}),
        ('User',{'fields':['user']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('title', 'pub_date', 'is_open')
    list_filter = ['pub_date']
    search_fields = ['title']

admin.site.register(Poll, PollAdmin)