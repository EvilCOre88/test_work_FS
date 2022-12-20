from rest_framework import serializers
from django.conf import settings
from django.core.exceptions import ValidationError

from .models import MailingList, Client, Message


class MailingListSerializer(serializers.ModelSerializer):

    class Meta:
        model = MailingList
        fields = ('id', 'mailing_date_time', 'message', 'filter_code', 'filter_tag', 'finish_date_time')


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = ('id', 'phone', 'code', 'tag', 'timezone')

class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ('id', 'send_date_time', 'status', 'mailing_list', 'client')


class MessageDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ('id', 'send_date_time', 'status', 'mailing_list', 'client')
        depth = 1


class MailingListDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = MailingList
        fields = ('id', 'mailing_date_time', 'message', 'filter_code', 'filter_tag', 'finish_date_time', 'messages')
        depth = 2


class SendSerializer(serializers.Serializer):
    mailing_list_id = serializers.IntegerField(min_value=1)