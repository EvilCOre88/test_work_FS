from test_work_FS.celery import app
from .models import Client, MailingList, Message, MessageStatusChoices
import requests, json

# @app.task
# def client_ids(mailing_list_id):
#     print('воркер не воркер')
#     mailing = MailingList.objects.filter(id__exact= mailing_list_id).first()
#     sent = []
#     not_sent = []
#     try:
#         client_list = Client.objects.filter(tag__iexact= mailing.filter_tag,
#                                             code__exact= mailing.filter_code)
#         if len(client_list) == 0:
#             return None
#         else:
#             messages = Message.objects.all()
#             for client in client_list:
#                 message_ids = [m.client.id for m in messages]
#                 mailing_ids = [m.mailing_list.id for m in messages]
#                 if client.id not in message_ids or (client.id in message_ids and mailing_list_id not in mailing_ids):
#                     add_message = Message(client= client, mailing_list= mailing)
#                     add_message.save()
#                     not_sent.append(client.id)
#                 else :
#                     message_status = Message.objects.filter(client__exact=client.id, mailing_list__exact=mailing_list_id).first()
#                     if message_status.status == 'NOT_SENT':
#                         not_sent.append(client.id)
#                     elif message_status.status == 'SENT':
#                         sent.append(client.id)
#             if len(sent) == 0:
#                 return not_sent
#             elif len(sent) == len(client_list):
#                 return True
#             elif len(not_sent) == len(client_list):
#                 return not_sent
#             else:
#                 return not_sent
#     except AttributeError:
#         return False
#
# @app.task
# def sending(client_id, mailing_message, headers):
#     message_id = Message.objects.filter(client__exact=client_id).first()
#     client_phone = Client.objects.filter(id__exact=client_id).first()
#     body = {
#         'id': message_id.id,
#         'phone': client_phone.phone,
#         'text': mailing_message
#     }
#     url = 'https://probe.fbrq.cloud/v1/send/{msgID}'
#     url = url.format(msgID=message_id.id)
#     res = requests.post(url, data=json.dumps(body), headers=headers)
#     print(client_id, mailing_message, headers)
#     if res.status_code == 200:
#         Message.objects.filter(client__exact=client_id).update(status='SENT')
#         return Response({'message': 'Сообщение отправлено!'},
#                         status=status.HTTP_200_OK)
#     else:
#         return Response({'message': 'Некоторые сообщения не отправлены, повторите попытку еще раз'},
#                         status=status.HTTP_206_PARTIAL_CONTENT)

def task_info(client_id, mailing_id):
    api_key = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDAxMjE0NzYsImlzcyI6ImZhYnJpcXVlIiwibmFtZSI6IkBIYXJkY29yZV9vdiJ9.M7kdGqylS_idbXNHARyTVnuRWngnJWK7MEFeOORbOtk'
    headers = {
        'Content-type': 'application/json',
        'Authorization': api_key,
        'cache-control': 'no-cache'
    }
    message_id = Message.objects.filter(client__exact=client_id).first()
    client_phone = Client.objects.filter(id__exact=client_id).first()
    mailing = MailingList.objects.filter(id__exact=mailing_id).first()
    body = {
        'id': message_id.id,
        'phone': client_phone.phone,
        'text': mailing.message
    }
    url = 'https://probe.fbrq.cloud/v1/send/{msgID}'
    url = url.format(msgID=message_id.id)
    return [url, body, headers]


def to_db(status_code, client_id):
    if status_code == 200:
        Message.objects.filter(client__exact=client_id).update(status='SENT')


@app.task
def sending(client_id, mailing_id):
    info = task_info(client_id, mailing_id)
    res = requests.post(info[0], data=json.dumps(info[1]), headers=info[2])
    to_db(res.status_code, client_id)
    return res.status_code
