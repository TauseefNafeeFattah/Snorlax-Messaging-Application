from django.contrib import admin
from .models import Message, Contact, Chat
# Register your models here.


class ChatAdmin(admin.ModelAdmin):
    filter_horizontal = ('participants',)


class ContactAdmin(admin.ModelAdmin):
    filter_horizontal = ('friends',)


admin.site.register(Message)
admin.site.register(Chat, ChatAdmin)
admin.site.register(Contact, ContactAdmin)
