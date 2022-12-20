from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class MailingList(models.Model):

    mailing_date_time = models.DateTimeField(verbose_name='Дата начала рассылки')
    message = models.TextField(verbose_name='Сообщение клиенту')
    filter_code = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(999)],
                                      verbose_name='Фильтр кода оператора',
                                      default=1)
    filter_tag = models.CharField(max_length=10,
                                  verbose_name='Фильтр тега')
    finish_date_time = models.DateTimeField(verbose_name='Дата окончания рассылки')

class Client(models.Model):

    phone = models.PositiveBigIntegerField(default=7,
                                           validators=[MinValueValidator(70000000000), MaxValueValidator(79999999999)],
                                           unique=True,
                                           verbose_name='Номер телефона')
    code = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(999)],
                                       verbose_name='Код оператора')
    tag = models.CharField(max_length=10,
                           verbose_name='Код оператора и тег')
    timezone = models.CharField(max_length=20,
                                verbose_name='Часовой пояс')


class MessageStatusChoices(models.TextChoices):

    SENT = 'SENT', 'Отправлено'
    NOT_SENT = 'NOT_SENT', 'Неотправлено'

class Message(models.Model):

    send_date_time = models.DateTimeField(auto_now=True,
                                          verbose_name='Дата/время создания/отправки сообщения')
    status = models.TextField(choices=MessageStatusChoices.choices,
                              default=MessageStatusChoices.NOT_SENT,
                              verbose_name='Статус отправки')
    mailing_list = models.ForeignKey(MailingList,
                                     on_delete=models.CASCADE,
                                     related_name='messages')
    client = models.ForeignKey(Client,
                               on_delete=models.CASCADE,
                               related_name='messages')
