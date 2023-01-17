import requests, json, time
from django.conf import settings
from django.shortcuts import render
from django.db import models
from rest_framework import status, mixins
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from celery import Celery
from datetime import datetime as dt
import datetime, pytz
from .tasks import sending

from .models import MailingList, Client, Message
from .serializers import MailingListSerializer, MailingListDetailSerializer, ClientSerializer, MessageSerializer, MessageDetailSerializer, SendSerializer


class MailingListViewSet(ModelViewSet):
    queryset = MailingList.objects.all()
    serializer_class = MailingListSerializer

    def delete(self, request):
        mailing = MailingList.objects.all()
        mailing_ids = [mail.id for mail in mailing]
        if request.method == 'DELETE' and request.data['id'] in mailing_ids:
            mailing = MailingList.objects.filter(id__exact= request.data['id'])
            mailing.delete()
            return Response({'message': 'Рассылка удалена!',
                             'request': request.data}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'message': 'Такой рассылки не существует!'}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        mailing = MailingList.objects.all()
        mailing_ids = [mail.id for mail in mailing]
        if request.method == 'PATCH' and request.data['id'] in mailing_ids:
            mailing = MailingList.objects.get(id=request.data['id'])
            try:
                mailing.mailing_date_time = request.data['mailing_date_time']
            except:
                pass
            try:
                mailing.message = request.data['message']
            except:
                pass
            try:
                mailing.filter_code = request.data['filter_code']
            except:
                pass
            try:
                mailing.filter_tag = request.data['filter_tag']
            except:
                pass
            try:
                mailing.finish_date_time = request.data['finish_date_time']
            except:
                pass
            mailing.save()
            return Response({'message': 'Рассылка изменена!',
                             'request': request.data}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'message': 'Такой рассылки не существует!'}, status=status.HTTP_204_NO_CONTENT)


class MailingListDetailViewSet(ModelViewSet):
    queryset = MailingList.objects.values('id', 'mailing_date_time', 'message', 'filter_code', 'filter_tag', 'finish_date_time', 'messages')
    serializer_class = MailingListDetailSerializer


class ClientViewSet(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def delete(self, request):
        clients = Client.objects.all()
        clients_ids = [client.id for client in clients]
        if request.method == 'DELETE' and request.data['id'] in clients_ids:
            client = Client.objects.filter(id__exact= request.data['id'])
            client.delete()
            return Response({'message': 'Клиент удален!',
                             'request': request.data}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'message': 'Такого клиента не существует!'}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        clients = Client.objects.all()
        clients_ids = [client.id for client in clients]
        if request.method == 'PATCH' and request.data['id'] in clients_ids:
            client = Client.objects.get(id=request.data['id'])
            try:
                client.phone = request.data['phone']
            except:
                pass
            try:
                client.code = request.data['code']
            except:
                pass
            try:
                client.tag = request.data['tag']
            except:
                pass
            try:
                client.timezone = request.data['timezone']
            except:
                pass
            client.save()
            return Response({'message': 'Клиент изменен!',
                             'request': request.data}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'message': 'Такого клиента не существует!'}, status=status.HTTP_204_NO_CONTENT)


class MessageViewSet(ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class MessageDetailViewSet(ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageDetailSerializer


def client_ids(mailing_list_id):
    mailing = MailingList.objects.filter(id__exact= mailing_list_id).first()
    sent = []
    not_sent = []
    try:
        client_list = Client.objects.filter(tag__iexact= mailing.filter_tag,
                                            code__exact= mailing.filter_code)
        if len(client_list) == 0:
            return None
        else:
            messages = Message.objects.all()
            for client in client_list:
                message_ids = [m.client.id for m in messages]
                mailing_ids = [m.mailing_list.id for m in messages]
                if client.id not in message_ids or (client.id in message_ids and mailing_list_id not in mailing_ids):
                    add_message = Message(client= client, mailing_list= mailing)
                    add_message.save()
                    not_sent.append(client.id)
                else :
                    message_status = Message.objects.filter(client__exact=client.id, mailing_list__exact=mailing_list_id).first()
                    if message_status.status == 'NOT_SENT':
                        not_sent.append(client.id)
                    elif message_status.status == 'SENT':
                        sent.append(client.id)
            if len(sent) == 0:
                return not_sent
            elif len(sent) == len(client_list):
                return True
            else:
                return not_sent
    except AttributeError:
        return False


@api_view(['GET', 'POST'])
def send_mail(request):

    if request.method == 'GET':
        return Response({'message': 'Этот путь поддерживает только метод POST'})
    elif request.method == 'POST':
        serializer = SendSerializer(data=request.data)
        if serializer.is_valid():
            mailing_id = request.data['mailing_list_id']
            mailing = MailingList.objects.filter(id__exact=mailing_id).first()
            if mailing is not None:
                mailing_id = request.data['mailing_list_id']
                message = client_ids(mailing_id)
                mail_from = mailing.mailing_date_time.strftime('%Y-%m-%d %H:%M:%S')
                mail_to = mailing.finish_date_time.strftime('%Y-%m-%d %H:%M:%S')
                if message is None:
                    return Response({'message': 'В данной рассылке нет клиентов по выбранным фильтрам'}, status=status.HTTP_400_BAD_REQUEST)
                elif message is True:
                    return Response({'message': 'В этой рассылке все сообщения уже были отправлены!'}, status=status.HTTP_204_NO_CONTENT)
                elif message is False:
                    return Response({'message': 'Такой рассылки не существует!'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    res = []
                    print(message)
                    for m in message:
                        tz = Client.objects.get(id= m)
                        tz = tz.timezone
                        if tz[0] == '-':
                            tz = '+' + tz[1:]
                        elif tz[0] == '+':
                            tz = '-' + tz[1:]
                        else:
                            res.append({'message': f'Укажите правильный часовой пояс в формате `+3` для клиента {m}'})
                            continue
                        zone = pytz.timezone(f'Etc/GMT{tz}')
                        send_time = dt.now(zone).strftime('%Y-%m-%d %H:%M:%S')
                        if send_time > mail_from and send_time < mail_to:
                            response = sending.delay(m, mailing_id)
                            response = response.get()
                            print(response)
                            if response == 400:
                                res.append({f'client_id {m}': f'Сообщение клиенту {m} не отправлено, пробуем еще раз'})
                            elif response ==  200:
                                res.append({f'client_id {m}': f'Сообщение для клиента {m} успешно отправлено!'})
                            elif response == 404:
                                res.append({f'client_id {m}': f'Некорректная страница запроса сервера для клиента {m}, повторите попытку'})
                            else:
                                res.append({f'client_id {m}': f'Странный респонс от сервера {status_list},'
                                                              f'для клиента {m} повторите попытку'})
                        elif send_time < mail_from:
                            countdown = dt.strptime(mail_from, '%Y-%m-%d %H:%M:%S') - dt.strptime(send_time, '%Y-%m-%d %H:%M:%S')
                            response = sending.apply_async((m, mailing_id), countdown= countdown.seconds)
                            if not response.ready():
                                res.append({f'client_id {m}': f'Сообщение для клиента {m} поставлено в очередь '
                                                            f'и будет отправлено {mail_from}'})
                        else:
                            res.append({f'client_id {m}': f'Время рассылки {mail_to} для клиента {m} уже окончено, '
                                                               f'измените время рассылки!'})
                    return Response({'message': res}, status=status.HTTP_202_ACCEPTED)
            else:
                return Response({'message': f'Рассылки номер {mailing_id} не существует!'},
                                status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


