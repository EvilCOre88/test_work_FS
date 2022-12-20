from django.contrib import admin

from .models import MailingList, Client, Message


@admin.register(MailingList)
class MailingListAdmin(admin.ModelAdmin):
    list_display = ('id', 'mailing_date_time', 'message', 'filter_code', 'filter_tag', 'finish_date_time')
    list_editable = ('mailing_date_time', 'message', 'filter_code', 'filter_tag', 'finish_date_time')

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone', 'code', 'tag', 'timezone')
    list_editable = ('phone', 'code', 'tag', 'timezone')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'send_date_time', 'status', 'mailing_list', 'client')

    def has_add_permission(self, request):
        return False